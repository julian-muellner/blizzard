from .bernoulli import Bernoulli
from .discrete_uniform import DiscreteUniform
from .distribution import Distribution
from .categorical import Categorical

__distributions__ = {
    "Bernoulli": Bernoulli,
    "DiscreteUniform": DiscreteUniform,
    "Categorical": Categorical
}

def distribution_factory(dist_name: str, parameters) -> Distribution:
    if dist_name in __distributions__:
        return __distributions__[dist_name](parameters)
    raise RuntimeError(f"Distribution {dist_name} is not supported")
