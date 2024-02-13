# 珍妮机API
# MoreParticleAPI
### A python api made for [more-particle](https://github.com/BottleSoy/more-particle) mod
### 用于更便捷地针对more particle mod进行自定义粒子制作

## 使用方法示例

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

func.add_event(pe)
world.add_function(func)
```
进入游戏后，使用`/function namespace:test`即可看到粒子效果
