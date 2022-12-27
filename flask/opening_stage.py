from pxr import Usd

#stage = Usd.Stage.CreateNew('sphere_sample.usda')

stage = Usd.Stage.Open('sphere_sample.usda')
stage.Save()
stage = Usd.Stage.Open('sphere_sample.usda')
# Do something to the stage
stage.Export('sphere_sample.usdc')