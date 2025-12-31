# executor_agent.py
import logging
from typing import Dict, Set

from ..planner.schemas import GraphSpec, NodeSpec
from ..registry import AGENT_REGISTRY

logger = logging.getLogger(__name__)


class GraphExecutor:
    """
    LangGraph-style DAG executor.
    """

    def __init__(self):
        self.state: Dict[str, any] = {}
        self.completed_nodes: Set[str] = set()

    async def execute(self, graph: GraphSpec) -> Dict[str, any]:
        """
        Execute the graph respecting dependencies.
        """
        # Initialize shared state
        self.state["goal"] = graph.goal
        self.state["num_slides"] = getattr(graph, "num_slides", 14)

        # Build dependency maps
        dependencies = {node_id: set() for node_id in graph.nodes}
        dependents = {node_id: set() for node_id in graph.nodes}

        for src, dst in graph.edges:
            dependencies[dst].add(src)
            dependents[src].add(dst)

        # Start with entry nodes
        ready = set(graph.entry_nodes)

        while ready:
            node_id = ready.pop()
            await self._execute_node(node_id, graph.nodes[node_id])

            self.completed_nodes.add(node_id)

            # Unlock dependent nodes
            for dependent in dependents.get(node_id, []):
                if dependencies[dependent].issubset(self.completed_nodes):
                    ready.add(dependent)

        return self.state

    async def _execute_node(self, node_id: str, node: NodeSpec):
        if node.agent not in AGENT_REGISTRY:
            raise NotImplementedError(f"Agent {node.agent} not implemented")

        agent_fn = AGENT_REGISTRY[node.agent]

        if agent_fn is None:
            logger.error("Agent %s is registered but implementation is None", node.agent)
            raise NotImplementedError(f"Agent {node.agent} implementation missing")

        # Build input payload
        input_payload = {
            "goal": self.state.get("goal"),
            "state": self.state,
        }

        # Entry nodes may have explicit input
        if node.input is not None:
            input_payload["input"] = node.input

        result = await agent_fn(input_payload)

        # Store output in shared state
        self.state[node_id] = result
        logger.debug("Node %s executed. Stored output under state[%s]", node.agent, node_id)