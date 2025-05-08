import json
import os.path

from enity.BlockItem import BlockItem
from tools.load import get_json_dir


class BlockManager:
    def __init__(self):
        """
        初始化一个方块管理器。
        """
        self.blocks = []  # 存储所有方块对象的列表

    def add_block(self, block):
        """
        添加一个方块到管理器中。
        :param block: Block 对象
        """
        self.blocks.append(block)

    def save_to_json(self, file_name):
        # 将每个方块转换为字典格式
        blocks_data = [block.to_dict() for block in self.blocks]
        # 将数据保存到文件
        with open(os.path.join(get_json_dir(), file_name), "w", encoding="utf-8") as file:
            json.dump(blocks_data, file, ensure_ascii=False, indent=4)

        print(f"成功保存 {len(self.blocks)} 个方块到 {file_name} 文件中！")

    def load_from_json(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                blocks_data = json.load(file)
            # 将字典数据转换为 Block 对象
            self.blocks = [BlockItem.from_dict(data) for data in blocks_data]

            print(f"成功从 {file_name} 文件中加载 {len(self.blocks)} 个方块！")
        except FileNotFoundError:
            print(f"文件未找到：{file_name}")
        except json.JSONDecodeError:
            print(f"文件内容不是有效的 JSON 格式：{file_name}")

    def __str__(self):
        """
        返回方块管理器的字符串表示。
        """
        return f"BlockManager(containing {len(self.blocks)} blocks)"