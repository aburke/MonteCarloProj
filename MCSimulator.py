from EquityCalculator import EquityCalculator
from CalculatorGroup import CalculatorGroup

class MCSimulator(object):
    def __init__(self):
        self.calculators = {
            'E': CalculatorGroup(EquityCalculator.calculateReturn
                                 , EquityCalculator.filterSet
                                 , EquityCalculator.genEquityParameters)
        }

    def runSimulation(self, dataSet, iterations):
        # Create dictionary of parameters for each calculator
        params = {i: x.genParameters(x.filterSet(dataSet)) for i, x in self.calculators.items()}

        # Run simulation with correspoding parameters for each calcReturn function
        def computeRetuns():
            return sum([x.calcReturn(**params[i]) for i, x in self.calculators.items()])

        return [computeRetuns() for _ in xrange(iterations)]

    def calcVaR(self, series, confidence):
        offset = 100 - confidence
        orderedSet = sorted(series, reverse=True)
        trials = len(series) + 1
        varIndex = int(trials - offset / 100.0 * trials) - 1

        return orderedSet[varIndex]