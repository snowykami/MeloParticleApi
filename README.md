# MoreParticleApi
### A python api made for [more-particle](https://github.com/BottleSoy/more-particle) mod
### 用于更便捷地针对more particle mod进行自定义粒子制作

## 使用方法示例

```python
from mp_api import Save, ColorLifeParticle, ParticleEvent, CColor, MCFunction

world = Save(
    path="path/to/world",
    datapack='datapack_name',
    namespace='namespace',
)

# 创建一个粒子
p = ColorLifeParticle(
    color=CColor.WHITE
)

pe = ParticleEvent(
    particle=p,
    pos=(0, 0, 0),
    speed=(0, 0, 0),
    count=1,
)

func = MCFunction(
    name='test',
)

func.add_event(pe)
world.add_function(func)
```
进入游戏后，使用`/function namespace:test`即可看到粒子效果