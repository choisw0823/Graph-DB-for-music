from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import P

# from gremlin_python.structure.io import graphson, kryo
import networkx as nx

import json
import csv 

class Neptune:
    def __init__(self):
        endpoint = 'wss://database-2.cluster-cc6bbeuwo4ac.ap-northeast-2.neptune.amazonaws.com:8182/gremlin'
        self.remoteConn = DriverRemoteConnection(endpoint,'g')
        try:
            self.g = Graph().traversal().withRemote(self.remoteConn)
        except Exception as e:
            print("Error connecting to Amazon Neptune:", e)
            exit()

    def find_id(self, label, key, properties):
        try:
            return self.g.V().hasLabel(label).has(key, properties).next()
        except Exception as e:
            print("Error finding id:", e)
            return None        

    def create_node(self, label, properties):
        try:
            node = self.g.addV(label)
            for key, value in properties.items():
                node = node.property(key, value)
            return node.next()
        except Exception as e:
            print("Error creating node:", e)
            return None
    
    def create_node_if_not_exists(self, label, find_key, find_property, properties):
    # Check if a node with the same property value already exists
        try:
            node = self.g.V().hasLabel(label).has(find_key, find_property).toList()

    # If the node does not exist, create a new one
            if not node:
                return self.create_node(label, properties)
            else:
                return False
        except Exception as e:
            print('Error creating Node : ', e)
            return None

    def create_unique_node(self, label, properties):
        try:
            return self.g.addV(label).property(properties).coalesce(
                __.V().hasLabel(label).has(properties),
                __.addV(label).property(properties)
            ).next()
        except Exception as e:
            print("Error creating unique node:", e)
            return None
    # def check_node_exist(self, label, properties):
    #     try:
    #         r = self.g.V().hasLabel(label).has(properties).next()
    #         if r:
    #             return r
    #         else:
    #             return False

    #     except Exception as e:
    #         print('Error checking node : ', e)
    #         return None


    def create_edge(self, outV, label, inV, properties):
        try:
            if properties is None:
                return self.g.addE(label).from_(__.V().hasId(outV)).to(__.V().hasId(inV)).next()
            else:
                e = self.g.addE(label).from_(__.V().hasId(outV)).to(__.V().hasId(inV))
                for key, value in properties.items():
                    e = e.property(key, value)
                return e.next()
        except Exception as e:
            print("Error creating edge:", e)
            return None
    
    def create_unique_edge(self, outV, label, inV, properties):
        try:
            if not self.g.V().hasId(outV).outE(label).inV().hasId(inV).hasNext():
                return self.create_edge(outV, label, inV, properties)
        except Exception as e:
            print('Error creating edge : ', e)
            return None
    
    def check_edge_exist(self, outV, label, inV):
        try:
            if self.g.V().hasId(outV).outE(label).inV().hasId(inV).hasNext():
                return True
            else:
                return False

        except Exception as e:
            print('Error checking edge : ', e)
            return None


    def create_two_way_edge(self, outV, label, inV, properties):
        try:
            edge1 = self.g.V(outV).addE(label).to(self.g.V(inV))
            for key, value in properties.items():
                edge1 = edge1.property(key, value)
            edge1 = edge1.next()
            
            edge2 = self.g.V(inV).addE(label).to(self.g.V(outV))
            for key, value in properties.items():
                edge2 = edge2.property(key, value)
            edge2 = edge2.next()
            
            return edge1,edge2
        except Exception as e:
            print("Error creating edge:", e)
            return None
    
    def update_node(self, id, properties):
        try:
            node = self.g.V(id)
            for key, value in properties.items():
                node = node.property(key, value)
            return node.next()
        except Exception as e:
            print("Error updating node:", e)
            return None
    
    def update_edge(self, id, properties):
        try:
            edge = self.g.E(id)
            for key, value in properties.items():
                edge = edge.property(key, value)
            return edge.next()
        except Exception as e:
            print("Error updating edge:", e)
            return None

    
    def get_node(self, id):
        try:
            return self.g.V(id).valueMap().next()
        except Exception as e:
            print("Error retrieving node:", e)
            return None

    def get_edge(self, id):
        try:
            return self.g.E(id).valueMap().next()
        except Exception as e:
            print("Error retrieving edge:", e)
            return None
            
    def drop_node(self, id):
        try:
            return self.g.V(id).drop().iterate()
        except Exception as e:
            print("Error dropping node:", e)
            return None

    def drop_edge(self, id):
        try:
            return self.g.E(id).drop().iterate()
        except Exception as e:
            print("Error dropping edge:", e)
            return None
    
    def get_all_nodes(self):
        try:
            return self.g.V().valueMap().toList()
        except Exception as e:
            print("Error getting all nodes:", e)
            return None
    
    def get_all_edges(self):
        try:
            return self.g.E().valueMap().toList()
        except Exception as e:
            print("Error getting all edges:", e)
            return None
    
    def drop_nodes_by_label(self, label):
        try:
            return self.g.V().hasLabel(label).drop().iterate()
        except Exception as e:
            print("Error dropping nodes:", e)
            return None

    def get_connected_vertices(self, vertex_id, edge_label):
        vertices = self.g.V().hasId(vertex_id).outE(edge_label).inV().valueMap().toList()
        return vertices
    
    def get_connected_vertices_reverse(self, vertex_id, edge_label):
        vertices = self.g.V().hasId(vertex_id).inE(edge_label).outV().valueMap().toList()
        return vertices
        
    def get_nodes_by_label(self, label):
        vertices =  self.g.V().hasLabel(label).valueMap().toList()
        return vertices

    def drop_all(self):
        self.g.V().drop().iterate()
        self.g.E().drop().iterate()


    def  __del__(self):
        self.remoteConn.close()


if __name__=='__main__':
    pass