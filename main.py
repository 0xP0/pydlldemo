# test.py

import ctypes
import os
import platform
import sys


def load_dynamic_library(lib_name: str, lib_dir: str = None, target_os: str = None):
    """
    根据目标操作系统加载动态库。

    :param lib_name: 动态库的基础名称（不包括前缀和扩展名）。
    :param lib_dir: 动态库所在的目录。如果未提供，默认使用脚本所在目录。
    :param target_os: 目标操作系统名称（'Windows', 'Linux', 'Darwin'）。如果未提供，使用当前系统。
    :return: 加载的动态库对象。
    :raises OSError: 如果无法加载动态库。
    """
    # 获取目标操作系统
    if target_os is None:
        target_os = platform.system()
    print(f"目标操作系统: {target_os}")

    # 设置动态库文件名和加载器
    if target_os == "Windows":
        lib_filename = f"{lib_name}.dll"
        loader = ctypes.WinDLL
    elif target_os == "Linux":
        lib_filename = f"lib{lib_name}.so"
        loader = ctypes.CDLL
    elif target_os == "Darwin":
        lib_filename = f"lib{lib_name}.dylib"
        loader = ctypes.CDLL
    else:
        raise OSError(f"不支持的目标操作系统: {target_os}")

    # 确定动态库的路径
    if lib_dir is None:
        # 使用脚本所在的目录
        lib_dir = os.path.dirname(os.path.abspath(__file__))
    lib_path = os.path.join(lib_dir, target_os.lower(), lib_filename)

    # 检查动态库是否存在
    if not os.path.isfile(lib_path):
        raise FileNotFoundError(f"无法找到动态库文件: {lib_path}")

    print(f"正在加载动态库: {lib_path}")

    try:
        dynamic_lib = loader(lib_path)
        print("动态库加载成功。")
        return dynamic_lib
    except OSError as e:
        raise OSError(f"无法加载动态库 {lib_path}: {e}")


def main():
    # 动态库的基础名称（不包括前缀和扩展名）
    lib_base_name = "example"

    # 动态库所在的目录（可选）。如果不指定，将使用脚本所在目录。
    lib_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")

    # 选择目标操作系统（当前系统或指定系统）
    current_os = platform.system()
    target_os = current_os  # 默认加载本地动态库

    # 如果需要加载特定平台的动态库，可以手动设置 target_os
    # 例如，在 macOS 上加载 Windows DLL（注意：这通常不可行，除非在兼容层中运行）
    # target_os = "Windows"

    try:
        # 加载动态库
        example_lib = load_dynamic_library(lib_base_name, lib_directory, target_os)

        # 定义函数原型
        # int add(int a, int b);
        example_lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
        example_lib.add.restype = ctypes.c_int

        # 调用函数
        a = 10
        b = 20
        result = example_lib.add(a, b)
        print(f"{a} + {b} = {result}")  # 输出: 10 + 20 = 30

    except (OSError, FileNotFoundError) as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
