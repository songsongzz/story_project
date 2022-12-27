from pxr import Usd

stage = Usd.Stage.Open('b.usd')
# do something to the stage
stage.Export('b.usda')