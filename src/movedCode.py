		lg.info ("initial bar2: " + str(a.getCurrentBar()))
		lg.info ("current bar2: " + str(i))
		
		# In a position and not in initial bar
		if a.inPosition() and a.getCurrentBar() < i:
			a.setClosePrices(action, currentPrice)
			lg.info("stops being used gain 1st:")
			lg.info(str(a.getStopGain()))
			lg.info(str(a.getStopLoss()))
			if currentPrice > a.getStopGain() or currentPrice < a.getStopLoss():
				lg.trigger(symbol, action, currentPrice, tm.now(), logPath)
				lg.info(str(symbol) + str(sellAction) + str(currentPrice) + str(tm.now()))
				# Position is closed
				a.closePosition()
				a.setCurrentBar(i)
				lg.info("Position Closed" + "\n")
