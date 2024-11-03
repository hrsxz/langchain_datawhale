# 使用 Python slim 版本作为基础镜像
FROM python:3.9-slim

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 创建 dev 用户并将其添加到 sudoers
# RUN useradd -ms /bin/bash dev
RUN useradd -ms /bin/bash dev && echo "dev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER dev

# 设置工作目录
WORKDIR /app

# 将项目文件复制到容器中
COPY . .

# 在 `site-packages` 中创建 `.pth` 文件
# RUN echo "/app" >> /usr/local/lib/python3.9/site-packages/project.pth

# 安装依赖
# RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量，避免生成 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE 1
# 设置环境变量，使 Python 输出日志不缓冲
ENV PYTHONUNBUFFERED 1
ENV CXXFLAGS="-std=c++11"

# # 启动应用的默认命令
# CMD ["python", "main.py"]
