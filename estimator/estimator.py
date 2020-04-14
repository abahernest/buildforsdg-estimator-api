def estimator_function(input_data):
    impact = {}
    severeImpact = {}
    ###Normalizing the duration to just days
    duration = duration_normaliser(input_data['periodType'],input_data['timeToElapse'])
    
    ##CHALLENGE 1
    ###calculating the estimated infections by the time duration
    ##IMPACT
    impact['currentlyInfected']=input_data['reportedCases'] * 10
    impact['infectionsByRequestedTime'] = impact['currentlyInfected']*(pow(2,duration//3))
    ##SEVEREIMPACT
    severeImpact['currentlyInfected']=input_data['reportedCases']*50
    severeImpact['infectionsByRequestedTime'] =severeImpact['currentlyInfected']*(pow(2,duration//3))
    
  
    ###CHALLENGE 2
    ##SEVEREIMPACT
    severeImpact['severeCasesByRequestedTime']=severeImpact['infectionsByRequestedTime']*0.15
  
    severeImpact['hospitalBedsByRequestedTime']=available_beds(input_data['totalHospitalBeds'],severeImpact['severeCasesByRequestedTime'])
    
    ##IMPACT
    impact['severeCasesByRequestedTime']=impact['infectionsByRequestedTime']*0.15
    
    impact['hospitalBedsByRequestedTime']=available_beds(input_data['totalHospitalBeds'],impact['severeCasesByRequestedTime'])
    

    ###CHALLENGE 3
    #function declaration for dolarsInFlight computation
    factor= money_lost(duration, input_data['avgDailyIncomeInUSD'], input_data['avgDailyIncomePopulation'])
    
    ##SEVEREIMPACT
    severeImpact['casesForICUByRequestedTime']=0.05*severeImpact['infectionsByRequestedTime']
    severeImpact['casesForVentilatorsByRequestedTime']=0.02*severeImpact['infectionsByRequestedTime']
    severeImpact['dollarsInFlight']=severeImpact['infectionsByRequestedTime']*factor
    
    ##IMPACT
    impact['casesForICUByRequestedTime']=0.05*impact['infectionsByRequestedTime']
    impact['casesForVentilatorsByRequestedTime']=0.02*impact['infectionsByRequestedTime']
    impact['dollarsInFlight']=impact['infectionsByRequestedTime']*factor
    
    
    output_data = {'input_data':input_data, 'impact':impact, 'severeImpact': severeImpact}
    return output_data

def duration_normaliser(duration ,value):
    if duration == "months" or duration =="month":
        value *= 30
        return value
    elif duration == "weeks" or duration=="week":
        value *= 7
        return value
    else:
        return value

def available_beds(totalbeds,severecases):
  #expected 35% bed availability in hospitals
    beds_available=(0.35*totalbeds)-severecases
    return beds_available

def money_lost(days,avgIncome,avgIncomePopulation):
  return avgIncome*days*avgIncomePopulation