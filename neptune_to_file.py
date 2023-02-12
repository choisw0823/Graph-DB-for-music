from neptune import Neptune

N = Neptune()
#N.export_to_csv('/home/ec2-user/Graph-DB-for-music/neptune_to_csv2')
#N.export_neptune_to_json_and_kryo('/home/ec2-user/Graph-DB-for-music/neptune_to_json.json', '/home/ec2-user/Graph-DB-for-music/neptune_to_kryo.kryo')
#N.export_neptune_to_json('/home/ec2-user/Graph-DB-for-music/neptune_to_json.json')
N.export_neptune_to_gexf('/home/ec2-user/Graph-DB-for-music/neptune_to_gexf.gexf')