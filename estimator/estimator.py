def estimator_function (input_data):
    """
                input_data is a dictionary of            
                    "name": ,
                    "avgAge": ,
                    "avgDailyIncomeInUSD": ,
                    "avgDailyIncomePopulation": ,
                    "periodType": ,
                    "timeToElapse": ,
                    "reportedCases": ,
                    "population": ,
                    "totalHospitalBeds": 
                
                This Fuction is the main engine of the API, it performs the necessary
                computations and estimations of the api and returns a dictionary that 
                contains the input_data, impact (estimated impact of virus), 
                and severeImpact (estimated severe impact of the virus).
    """
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
    severeImpact['severeCasesByRequestedTime']=int(severeImpact['infectionsByRequestedTime']*0.15)
  
    severeImpact['hospitalBedsByRequestedTime']=available_beds(input_data['totalHospitalBeds'],severeImpact['severeCasesByRequestedTime'])
    
    ##IMPACT
    impact['severeCasesByRequestedTime']=int(impact['infectionsByRequestedTime']*0.15)
    
    impact['hospitalBedsByRequestedTime']=available_beds(input_data['totalHospitalBeds'],impact['severeCasesByRequestedTime'])
    

    ###CHALLENGE 3
    #function declaration for dolarsInFlight computation
    factor= money_lost(duration, input_data['avgDailyIncomeInUSD'], input_data['avgDailyIncomePopulation'])
    
    ##SEVEREIMPACT
    severeImpact['casesForICUByRequestedTime']=int(0.05*severeImpact['infectionsByRequestedTime'])
    severeImpact['casesForVentilatorsByRequestedTime']=int(0.02*severeImpact['infectionsByRequestedTime'])
    severeImpact['dollarsInFlight']=int(severeImpact['infectionsByRequestedTime']*factor)
    
    ##IMPACT
    impact['casesForICUByRequestedTime']=int(0.05*impact['infectionsByRequestedTime'])
    impact['casesForVentilatorsByRequestedTime']=int(0.02*impact['infectionsByRequestedTime'])
    impact['dollarsInFlight']=int(impact['infectionsByRequestedTime']*factor)
    
    
    output_data = {'input_data':input_data, 'impact':impact, 'severeImpact': severeImpact}
    return output_data

def duration_normaliser(duration ,value):
    hash={"months":30,"month":30,"weeks":7,"week":7,"days":1,"day":1}
    if duration in hash:
        if value<0:
            return hash[duration]
        else:
            value *= hash[duration]
            return value
    else:
        if value>=0:
            return value
        else:
            return 0

def available_beds(totalbeds,severecases):
    #expected 35% bed availability in hospitals
    if totalbeds>=0 and severecases>=0:
        beds_available=(0.35*totalbeds)-severecases
        return int(beds_available)
    else:
        return 0

def money_lost(days,avgIncome,avgIncomePopulation):
    if days>0:
        return (avgIncome*avgIncomePopulation)/days
    else:
        return 0