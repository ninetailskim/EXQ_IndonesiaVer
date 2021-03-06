# 参赛作品名
《【AI创造营】当二仙桥遇上印尼电信广告》
## 作品简介
二仙桥大爷听着印尼电信广告就上了成华大道，谭警官拦都拦不住，使用paddlehub 检测人物已经分割，让你不用剪辑软件就能制作印尼电信广告风的视频
## 使用方式
```
python makeVideo.py --lh imgs/d.png --rh imgs/t.png --lb imgs/lback.png --rb imgs/rback.png --txt txts/exq.txt --output exq.mp4
python makeVideo.py --lh 左边的人的图片 --rh 右边的人的图片 --lb 左边的人的背景图 --rb 右边的人的背景图 --txt 对话文件 --output 生成的视频名称A
```


#### 这样就生成了视频，不过这样是没有声音的，我们来给他注（jia）入（shang）灵（yin）魂（yue）!
```
python addbgm.py --video exq.mp4 --bgm bgms/indonesia.mp3 --output bexq.mp4
python addbgm.py --video 生成的视频名称A --bgm 背景音乐文件 --output 最终的文件名
```

#### 注入了灵魂，所有的工作都完成啦

## 注意点
#### 1.lb和rb这两张的图片大小要是一样的才行   
#### 2.对话的格式
    A：右侧的人
    B：左侧的人
    格式：
        AXXXXXXXXXXX
        BYYYYYYYYYYY
####    这就代表了右侧的人说了XXXXXXXXXXX,左侧的人说了YYYYYYYYYYY
####    看了txts文件夹中的格式你就懂啦
#### 3.如果报字体找不到的问题，可以试试repo中提供的那个宋体simsun.ttc


## 其他的
#### utils下提供了一个很小的提取字幕的代码，可以自己试试，可能需要改一个很小的地方哈哈哈
