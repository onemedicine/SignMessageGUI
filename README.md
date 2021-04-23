# 
## 依赖安装
- apt-get install python3-pip  
这里python需要3.6以上 源于web3的限制
- pip3 install pipenv
- pipenv install --three --skip-lock

## 运行
- pipenv run python signUI.py   

## 打包exe
```shell
pyinstaller --hidden-import "web3" -i ./image/favicon.ico -F -w ./signUI.py
```
