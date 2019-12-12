import json
import struct
import lzma
import bpy
import bmesh

start_offset = -8
lzma_header = b']\x00\x00'

class Input(object):
  def __init__(self,flagList):
    self.flagList=flagList
    self.type=None
    self.debug=None
    self.imageList=[]
    self.type='string'
    self.filename=flagList

def Output(object):
  return object

def parse(filename):
    with open(filename, "rb") as binary_file:
        if binary_file.read(3) == lzma_header:
            parse_lzma(filename)
        else:
            process(binary_file)

def parse_lzma(filename):
    with lzma.open(filename, "rb") as binary_file:
        process(binary_file)

def process(binary_file):
    binary_file.seek(start_offset, 2)
    h_json_length = binary_file.read(4)
    # print(h_json_length)

    json_length = int.from_bytes(h_json_length, byteorder='little')
    # print(json_length)

    binary_file.seek(-json_length + start_offset, 2)
    h_json = binary_file.read(json_length)
    # print(h_json)

    my_json = h_json.decode('utf8')
    # print(my_json)

    data = json.loads(my_json)

    binary_file.seek(data['faceCount']['o'], 0)
    face_count = int.from_bytes(binary_file.read(data['faceCount']['l']), byteorder='little')
    # print(face_count)

    verticies = []

    i = 0
    while i < data['positions']['l'] / 4:
        v = 0
        vertex = []
        while v < 3:
            binary_file.seek(data['positions']['o'] + (i * 4), 0)
            vertex.append(float(''.join(map(str, (struct.unpack('f', binary_file.read(4)))))))
            v += 1
            i += 1
        # print(vertex)
        verticies.append(vertex)
    # print(verticies)

    faces = []

    i = 0
    while i < data['faces']['l'] / data['faces']['b']:
        f = 0
        face = []
        while f < face_count:
            binary_file.seek(data['faces']['o'] + (i * data['faces']['b']), 0)
            face.append(int.from_bytes(binary_file.read(data['faces']['b']), byteorder='little'))
            f += 1
            i += 1
        # print(face)
        faces.append(face)
    # print(faces)

    mesh = bpy.data.meshes.new('bingeom')
    ob = bpy.data.objects.new(mesh.name,mesh)
    col = bpy.data.collections.get('Collection')
    col.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    mesh.from_pydata(verticies, [], faces)
    mesh.validate()
    mesh.update()


def openFile(flagList):
    global input,output
    input = Input(flagList)
    output = Output(flagList)
    parse(input.filename)
