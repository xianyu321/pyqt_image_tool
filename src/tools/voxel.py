from PyQt5.QtGui import QVector3D


class Voxel:
    # 静态属性：顶点坐标和UV值
    front = 'front'
    back = 'back'
    top = 'up'
    bottom = 'down'
    left = 'left'
    right = 'right'
    vertices = [
        QVector3D(-0.5, -0.5, -0.5),  # 0: 左下后
        QVector3D(0.5, -0.5, -0.5),   # 1: 右下后
        QVector3D(0.5, 0.5, -0.5),    # 2: 右上后
        QVector3D(-0.5, 0.5, -0.5),   # 3: 左上后
        QVector3D(-0.5, -0.5, 0.5),   # 4: 左下前
        QVector3D(0.5, -0.5, 0.5),    # 5: 右下前
        QVector3D(0.5, 0.5, 0.5),     # 6: 右上前
        QVector3D(-0.5, 0.5, 0.5)     # 7: 左上前
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # 底面
        (4, 5), (5, 6), (6, 7), (7, 4),  # 顶面
        (0, 4), (1, 5), (2, 6), (3, 7)   # 垂直边
    ]

    # 静态属性：面索引
    faces = {
        'front': {
            'index': 0,
            'vertices_indices': [4, 5, 6, 7],  # 左下前、右下前、右上前、左上前
            'uvs': [(0, 0), (1, 0), (1, 1), (0, 1)]  # 假设使用相同的UV映射
        },
        'back': {
            'index': 1,
            'vertices_indices': [1, 0, 3, 2],  # 右下后、左下后、左上后、右上后
            'uvs': [(0, 0), (1, 0), (1, 1), (0, 1)]
        },
        'up': {
            'index': 2,
            'vertices_indices': [7, 6, 2, 3],  # 左上前、右上前、右上后、左上后
            'uvs': [(0, 0), (1, 0), (1, 1), (0, 1)]
        },
        'down': {
            'index': 3,
            'vertices_indices': [4, 5, 1, 0],  # 左下前、右下前、右下后、左下后
            'uvs': [(0, 0), (1, 0), (1, 1), (0, 1)]
        },
        'left': {
            'index': 4,
            'vertices_indices': [0, 4, 7, 3],  # 左下后、左下前、左上前、左上后
            'uvs': [(0, 0), (1, 0), (1, 1), (0, 1)]
        },
        'right': {
            'index': 5,
            'vertices_indices': [5, 1, 2, 6],  # 右下前、右下后、右上后、右上前
            'uvs': [(0, 0), (1, 0), (1, 1), (0, 1)]
        }
    }

    triangle_index = [[0, 1, 2],[0, 2, 3]]

    @classmethod
    def get_face(self, face_name):
        face = self.faces[face_name]
        vertices_indices = face['vertices_indices']
        uvs = face['uvs']
        return vertices_indices, uvs

    @classmethod
    def get_all_face(self):
        vertices_arr = []
        uvs_arr = []
        for face in self.faces.values():
            vertices_arr.append(face['vertices_indices'])
            uvs_arr.append(face['uvs'])
        return vertices_arr, uvs_arr