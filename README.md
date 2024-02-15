# 珍妮机API

### A python api made for [more-particle](https://github.com/BottleSoy/more-particle) mod

### 用于更便捷地针对more particle mod进行自定义粒子制作

# 快速上手

```python
from mp_api import Save, ColorLifeParticle, ParticleEvent, CColor, MCFunction

# 加载一个存档
world = Save(
    path="path/to/world",
    datapack='datapack_name',
    namespace='namespace',
)

# 实例化一个粒子
p = ColorLifeParticle(
    color=CColor.WHITE
)

# 创建一个粒子事件
pe = ParticleEvent(
    particle=p,
    pos=(0, 0, 0),
    speed=(0, 0, 0),
    count=1,
)

# 创建一个mcfunction用于存放事件
func = MCFunction(
    name='test',
)

func.add_events(pe)
world.add_function(func)
```

进入游戏后，使用`/function namespace:test`即可看到粒子效果

# 详细文档
## 索引
- [mp_api.draw](#module-mpapidraw)
- [mp_api.event](#module-mpapievent)

## module `mp_api.draw`

### class `Color()`
- 说明 实例化颜色类
- 参数
  - `color` 符合规范的颜色输入或一个颜色实例化的对象，详细可以参考`mp_api.mp_typing.T_Color`


- def `get_int(self, alpha: bool = False) -> int` 获取颜色的整数表示
    - 参数
        - `alpha` 是否包含透明度
    - 返回值
        - `int` 颜色的整数表示


- def `get_hex(self, alpha: bool = True, hashtag: bool = True) -> str` 获取颜色的十六进制表示
    - 参数
        - `alpha` 是否包含透明度
        - `hashtag` 是否包含`#`
    - 返回值
        - `str` 颜色的十六进制表示


- def `get_tuple(self, alpha: bool = False) -> T_RGB | T_ARGB` 获取颜色的元组表示
    - 参数
        - `alpha` 是否包含透明度
    - 返回值
        - `T_RGB | T_ARGB` 颜色的元组表示


- def `gradient_interpolation(self, other: T_Color | Color, p: float) -> Color` 获取两个颜色的插值
    - 参数
        - `color` 略
        - `p` 插值系数 0~1
    - 返回值
        - `Color` 插值后的颜色


### class `CColor`
- 说明 颜色类，用于存放一些常用颜色
- attribute
    - `BLACK: Color` 黑色
    - `WHITE: Color` 白色
    - `RED: Color` 红色
    - `GREEN: Color` 绿色
    - `BLUE: Color` 蓝色
    - `YELLOW: Color` 黄色
    - `CYAN: Color` 青色
    - `MAGENTA: Color` 洋红色
    - `ORANGE: Color` 橙色
    - `PURPLE: Color` 紫色
    - `PINK: Color` 粉色
    - `GRAY: Color` 灰色
    - `BROWN: Color` 棕色

## module `mp_api.event`

### class `BaseEvent(object)`
- 说明 事件基类
- def `__init__(self, time: int = 0)`
    - 参数
        - `time` 事件发生的时间
- property 
  - `command` 事件的命令

### class `ExecuteEvent(BaseEvent)`
- 说明 execute事件
- def `__init__(self, sub_commands: List[str], run_event: BaseEvent, **kwargs)`
    - 说明 实例化execute事件
    - 参数
        - `sub_commands` execute的子命令
        - `run_event` 执行的事件
        - `**kwargs` 调用基类super()方法的传参
    - 返回
      - `None`
    