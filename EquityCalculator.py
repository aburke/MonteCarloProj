class EquityCalculator(object):
    @staticmethod
    def computeMetrics(dataSet):
        # Get mean and standard deviation of prices on each stock
        metrics = dataSet.groupby('Tckr').agg({'Close': [np.mean, np.std]})['Close'].reset_index()

        # Get latest Quantity and Price for each stock
        currVals = pd.DataFrame(dataSet[dataSet['Date'] == dataSet['Date'].max()][['Quantity', 'Close', 'Tckr']])
        currVals['mktVal'] = currVals['Quantity'] * currVals['Close']

        return pd.merge(metrics, currVals, how='inner', on='Tckr')

    @staticmethod
    def calculateReturn(**kwargs):
        metrics = kwargs['dataSet']

        # calculate the return for equities in portfolio for price at T+1
        # assumes equity prices are normally distributed
        return sum((np.random.normal(metrics['mean'], metrics['std']) * metrics['Quantity'] - metrics['mktVal'])
                   / metrics['mktVal'])

    @staticmethod
    def filterSet(dataSet):
        return dataSet[dataSet['Type'] == 'E']

    @staticmethod
    def genEquityParameters(dataSet):
        return {'dataSet': EquityCalculator.computeMetrics(dataSet)}