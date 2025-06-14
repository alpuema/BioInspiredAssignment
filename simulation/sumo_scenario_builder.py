import os
import subprocess
import xml.etree.ElementTree as ET

class SumoScenarioBuilder:
    """
    Builds SUMO scenario files (nodes, edges, network, routes, config) from a scenario dict.
    """

    def __init__(self, scenario, output_dir="sumo_tmp"):
        """
        Args:
            scenario (dict): Scenario dictionary with keys 'nodes', 'edges', 'vehicles_per_hour', etc.
            output_dir (str): Where to output all generated SUMO files.
        """
        self.scenario = scenario
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def build(self):
        """
        Generates all necessary SUMO files and returns the path to the generated .sumocfg config file.
        """
        nodes_path = os.path.join(self.output_dir, "nodes.nod.xml")
        edges_path = os.path.join(self.output_dir, "edges.edg.xml")
        net_path = os.path.join(self.output_dir, "network.net.xml")
        routes_path = os.path.join(self.output_dir, "routes.rou.xml")
        sumocfg_path = os.path.join(self.output_dir, "scenario.sumocfg")

        self._write_nodes(nodes_path)
        self._write_edges(edges_path)
        self._generate_net(nodes_path, edges_path, net_path)
        self._write_routes(routes_path)
        self._write_sumocfg(net_path, routes_path, sumocfg_path)

        return sumocfg_path

    def _write_nodes(self, nodes_path):
        """
        Writes nodes.nod.xml from the scenario dictionary.
        """
        root = ET.Element("nodes")
        for node in self.scenario["nodes"]:
            attrib = {
                "id": f"{node[0]}_{node[1]}",
                "x": str(node[0] * 100),
                "y": str(node[1] * 100)
            }
            ET.SubElement(root, "node", attrib)
        tree = ET.ElementTree(root)
        tree.write(nodes_path, encoding="UTF-8", xml_declaration=True)

    def _write_edges(self, edges_path):
        """
        Writes edges.edg.xml from the scenario dictionary.
        """
        root = ET.Element("edges")
        for edge in self.scenario["edges"]:
            from_id = f"{edge[0][0]}_{edge[0][1]}"
            to_id = f"{edge[1][0]}_{edge[1][1]}"
            attrib = {
                "id": f"{from_id}_{to_id}",
                "from": from_id,
                "to": to_id,
                "numLanes": str(edge[2] if len(edge) > 2 else 1),
                "speed": str(edge[3] if len(edge) > 3 else 13.9)
            }
            ET.SubElement(root, "edge", attrib)
        tree = ET.ElementTree(root)
        tree.write(edges_path, encoding="UTF-8", xml_declaration=True)

    def _generate_net(self, nodes_path, edges_path, net_path):
        """
        Uses netconvert to generate SUMO network file.
        """
        cmd = [
            "netconvert",
            "--node-files", nodes_path,
            "--edge-files", edges_path,
            "--output-file", net_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"netconvert failed: {result.stderr}")

    def _write_routes(self, routes_path):
        """
        Writes routes.rou.xml with vehicle types, routes, and vehicle flows.
        This basic version assigns all vehicles to a single route (you can extend it).
        """
        n = int(len(self.scenario["nodes"]) ** 0.5)
        vph = self.scenario.get("vehicles_per_hour", 1000)
        duration = self.scenario.get("duration", 3600)
        flow_interval = duration / max(vph, 1)

        with open(routes_path, "w", encoding="utf-8") as f:
            f.write('<routes>\n')
            # Define vehicle type
            f.write('  <vType id="car" accel="1.0" decel="4.5" length="5" minGap="2.5" maxSpeed="13.9" guiShape="passenger"/>\n')

            # Define a basic route (extend for more complex scenarios)
            edge_ids = self._get_main_route_edge_ids(n)
            f.write(f'  <route id="r0" edges="{" ".join(edge_ids)}"/>\n')

            # Generate vehicles
            num_vehicles = vph // (3600 // duration)
            for k in range(num_vehicles):
                depart = round(k * flow_interval, 2)
                f.write(f'  <vehicle id="veh{k}" type="car" route="r0" depart="{depart}"/>\n')
            f.write('</routes>\n')

    def _get_main_route_edge_ids(self, n):
        """
        Example: Returns a list of edge IDs for a straight route along top row and last column.
        """
        edge_ids = []
        # Horizontal (top row)
        for i in range(n - 1):
            edge_ids.append(f"{i}_0_{i+1}_0")
        # Vertical (last column)
        for j in range(n - 1):
            edge_ids.append(f"{n-1}_{j}_{n-1}_{j+1}")
        return edge_ids

    def _write_sumocfg(self, net_path, routes_path, sumocfg_path):
        """
        Writes the SUMO .sumocfg configuration file.
        """
        config_xml = f"""<configuration>
  <input>
    <net-file value="{os.path.basename(net_path)}"/>
    <route-files value="{os.path.basename(routes_path)}"/>
  </input>
  <time>
    <begin value="0"/>
    <end value="{self.scenario.get("duration", 3600)}"/>
  </time>
</configuration>
"""
        with open(sumocfg_path, "w", encoding="utf-8") as f:
            f.write(config_xml)
