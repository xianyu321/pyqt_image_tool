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


# 创建一些方块
grass_block = BlockItem(
    name="GrassBlock",
    top="grass_top_texture",
    bottom="dirt_texture",
    front="grass_side_texture",
    back="grass_side_texture",
    left="grass_side_texture",
    right="grass_side_texture"
)

stone_block = BlockItem(
    name="StoneBlock",
    top="stone_texture",
    bottom="stone_texture",
    front="stone_texture",
    back="stone_texture",
    left="stone_texture",
    right="stone_texture"
)

water_block = BlockItem(
    name="WaterBlock",
    top="water_texture",
    bottom="water_texture",
    front="water_texture",
    back="water_texture",
    left="water_texture",
    right="water_texture"
)

# 创建一个方块管理器
manager = BlockManager()

# 添加方块到管理器
manager.add_block(grass_block)
manager.add_block(stone_block)
manager.add_block(water_block)

# 保存方块到 JSON 文件
manager.save_to_json("blocks.json")

# 加载方块从 JSON 文件
new_manager = BlockManager()
new_manager.load_from_json("blocks.json")

# 打印加载的方块信息
for block in new_manager.blocks:
    print(block)