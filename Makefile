# Makefile

# 定义变量
LIB_NAME := example
SRC := example.c
HEADERS := example.h
BUILD_DIR := build
WINDOWS_DIR := $(BUILD_DIR)/windows
LINUX_DIR := $(BUILD_DIR)/linux
MACOS_DIR := $(BUILD_DIR)/darwin

# 默认编译器
CC := gcc

# 交叉编译器（用于编译 Windows DLL）
CROSS_CC := x86_64-w64-mingw32-gcc

# 设置默认目标为 'default'
.DEFAULT_GOAL := default

# 检测主机操作系统
ifeq ($(OS),Windows_NT)
    CURRENT_OS := windows
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        CURRENT_OS := linux
    else ifeq ($(UNAME_S),Darwin)
        CURRENT_OS := darwin
    else
        $(error Unsupported OS: $(UNAME_S))
    endif
endif

# 默认目标：编译当前平台的动态库
default: $(CURRENT_OS)

# 目标：编译 Windows DLL
windows:
	@command -v $(CROSS_CC) >/dev/null 2>&1 || { \
		echo >&2 "MinGW-w64 compiler not found. Install it first."; \
		exit 1; \
	}
	@echo "Compiling Windows DLL..."
	mkdir -p $(WINDOWS_DIR)
	$(CROSS_CC) -shared -o $(WINDOWS_DIR)/$(LIB_NAME).dll $(SRC) -I. -D_WIN32
	@echo "Windows DLL generated at $(WINDOWS_DIR)/$(LIB_NAME).dll"

# 目标：编译 Linux 共享库
linux:
	@echo "Compiling Linux shared object..."
	mkdir -p $(LINUX_DIR)
	$(CC) -shared -fPIC -o $(LINUX_DIR)/lib$(LIB_NAME).so $(SRC) -I.
	@echo "Linux shared object generated at $(LINUX_DIR)/lib$(LIB_NAME).so"

# 目标：编译 macOS 动态库
darwin:
	@echo "Compiling macOS dynamic library..."
	mkdir -p $(MACOS_DIR)
	$(CC) -dynamiclib -o $(MACOS_DIR)/lib$(LIB_NAME).dylib $(SRC) -I.
	@echo "darwin dynamic library generated at $(MACOS_DIR)/lib$(LIB_NAME).dylib"

# 目标：编译所有平台的动态库
all: windows linux darwin
	@echo "All dynamic libraries have been compiled."

# 目标：清理构建目录
clean:
	@echo "Cleaning up build directories..."
	rm -rf $(BUILD_DIR)
	@echo "Build directories cleaned."

# 声明伪目标
.PHONY: all windows linux darwin clean default