from typing import Dict
from pymantic import sparql

server = sparql.SPARQLServer(
    'http://35.193.99.49:9999/blazegraph/namespace/kb/sparql')

# Loading data to Blazegraph
server.update(
    'load <https://github.com/dnswd/semanthink/raw/main/hospital-ratings-rdf-5.ttl>')

prefixes = '''
	PREFIX : <http://example.org/>
	PREFIX schema: <http://schema.org/>
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
	PREFIX dbo:  <http://dbpedia.org/ontology/> 
	PREFIX dpb:  <http://dbpedia.org/property/>
	PREFIX dbr: <http://dbpedia.org/resource/>
'''


def query(q):
    return server.query(prefixes + q)

def rs_res(res):
    return [(r['s']['value'], r['rs']['value']) for r in res['results']['bindings']]

def get_states():
    GET_STATES = '''
				SELECT DISTINCT ?stateName
				WHERE {
					?s :state ?state .
					?state foaf:name ?stateName .
				} ORDER BY ?stateName
			'''
    states = query(GET_STATES)
    return [state['stateName']['value'] for state in states['results']['bindings']]

def get_cities():
    GET_CITIES = '''
				SELECT DISTINCT ?cityName
				WHERE {
					?s :city ?city .
					?city foaf:name ?cityName .
				} ORDER BY ?cityName
			'''
    cities = query(GET_CITIES)
    return [city['cityName']['value'] for city in cities['results']['bindings']]

def get_cities_in_dbpedia():
    GET_CITIES = '''
				SELECT distinct ?city {
					?rs :city ?city .
					FILTER(regex(str(?city), "http://dbpedia.org"))
				}
    		'''
    cities = query(GET_CITIES)
    return [city['city']['value'] for city in cities['results']['bindings']]

def get_counties_in_dbpedia():
    GET_COUNTIES = '''
				SELECT distinct ?county {
					?rs :county ?county .
					FILTER(regex(str(?county), "http://dbpedia.org"))
				}
    		'''
    cities = query(GET_COUNTIES)
    return [city['county']['value'] for city in cities['results']['bindings']]

def get_tipes():
    GET_TYPES = '''
				SELECT DISTINCT ?tipe
				WHERE {
					?rs :type ?tipe .
				} ORDER BY ?tipe
			'''
    tipes = query(GET_TYPES)
    return [tipe['tipe']['value'] for tipe in tipes['results']['bindings']]

def get_ownerships():
    GET_OWNERSHIPS = '''
				SELECT DISTINCT ?ownership
				WHERE {
					?rs :ownership ?ownership .
				} ORDER BY ?ownership
			'''
    ownerships = query(GET_OWNERSHIPS)
    return [ownership['ownership']['value'] for ownership in ownerships['results']['bindings']]

def get_ratings():
    GET_RATINGS = '''
				SELECT DISTINCT ?rating
				WHERE {
					?rs :rating ?rating .
				} ORDER BY DESC(?rating)
			'''
    ratings = query(GET_RATINGS)
    return [rating['rating']['value'] for rating in ratings['results']['bindings']]

def get_emergency():
    GET_EMERGENCIES = '''
				SELECT DISTINCT ?emergency
				WHERE {
					?rs :hasEmergencyServices ?emergency .
				} ORDER BY DESC(?emergency)
			'''
    emergency = query(GET_EMERGENCIES)
    return [emergency['emergency']['value'] for emergency in emergency['results']['bindings']]

def get_rs(rs):
    GET_RS = '''
			SELECT ?s ?rs
			WHERE {
				?s a <http://dbpedia.org/resource/Hospital> .
				?s foaf:name ?rs .
				FILTER (regex(str(?rs), "%s", "i"))
			} ORDER BY ?rs
		''' % rs
    return rs_res(query(GET_RS))

def get_rs_by_state(state):
    GET_STATE = '''
				SELECT ?s ?rs
				WHERE {
					?s :state ?state .
					?state foaf:name "%s" .
					?s foaf:name ?rs .
				} ORDER BY ?rs
			''' % state
    return rs_res(query(GET_STATE))

def get_rs_by_city(city):
    GET_CITY = '''
				SELECT ?s ?rs
				WHERE {
					?s :city ?city .
					?city foaf:name "%s" .
					?s foaf:name ?rs .
				} ORDER BY ?rs
			''' % city
    return rs_res(query(GET_CITY))

def get_rs_by_tipe(tipe):
    GET_TYPE = '''
				SELECT ?s ?rs
				WHERE {
					?s :type "%s" .
					?s foaf:name ?rs .
				} ORDER BY ?rs
			''' % tipe
    return rs_res(query(GET_TYPE))

def get_rs_by_ownership(ownership):
    GET_OWNERSHIP = '''
				SELECT ?s ?rs
				WHERE {
					?s :ownership "%s" .
					?s foaf:name ?rs .
				} ORDER BY ?rs
			''' % ownership
    return rs_res(query(GET_OWNERSHIP))

def get_rs_by_rating(rating):
    GET_RATING = '''
				SELECT ?s ?rs
				WHERE {
					?s :rating %s .
					?s foaf:name ?rs .
				} ORDER BY ?rs
			''' % rating
    return rs_res(query(GET_RATING))

def get_rs_by_emergency(emergency):
    GET_EMERGENCY = '''
				SELECT ?s ?rs
				WHERE {
					?s :hasEmergencyServices "%s" .
					?s foaf:name ?rs .
				} ORDER BY ?rs
			''' % emergency
    return rs_res(query(GET_EMERGENCY))

def get_rs_by_ehr(ehr):
    GET_EHR = '''
				SELECT ?s ?rs
				WHERE {
					?s :meetsMeaningfulUseOfEHRs "Y" .
					?s foaf:name ?rs .
				} ORDER BY ?rs
			'''
    return rs_res(query(GET_EHR))

def get_hospital_count():
    GET_HOSPITAL_COUNT = '''
		SELECT (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
		}
	'''
    hospitalCountQuery = query(GET_HOSPITAL_COUNT)
    return int(hospitalCountQuery['results']['bindings'][0]['hospitalCount']['value'])

def get_er_count():
    GET_ER_COUNT = '''
		SELECT (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
			?hospital :hasEmergencyServices ?hasEr .
			FILTER(?hasEr="Yes"^^xsd:string)
		}
	'''
    getErCountQuery = query(GET_ER_COUNT)
    return int(getErCountQuery['results']['bindings'][0]['hospitalCount']['value'])

def get_patient_experiences_and_count():
    GET_PATIENT_EXPERIENCES_AND_COUNT = '''
		SELECT ?patientRating (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
			?hospital :patientExperience ?patientRating .
		} GROUP BY ?patientRating
	'''
    getPatientExperiencesAndCountQuery = query(
        GET_PATIENT_EXPERIENCES_AND_COUNT)
    result = {}
    patientExperinceLabel = [i['patientRating']['value']
                             for i in getPatientExperiencesAndCountQuery['results']['bindings']]
    patientExperienceCount = [i['hospitalCount']['value']
                              for i in getPatientExperiencesAndCountQuery['results']['bindings']]
    result['experienceLabel'] = patientExperinceLabel
    result['experienceCount'] = patientExperienceCount
    return result

def get_hospital_overall_rating_and_count():
    GET_HOSTPITAL_OVERALL_RATING_AND_COUNT = '''
		SELECT ?rating (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
			?hospital :rating ?rating .
		} GROUP BY ?rating
	'''
    getHospitalRatingsAndCountQuery = query(
        GET_HOSTPITAL_OVERALL_RATING_AND_COUNT)
    result = {}
    hospitalRatingLabel = [i['rating']['value']
                           for i in getHospitalRatingsAndCountQuery['results']['bindings']]
    hospitalRatingCount = [i['hospitalCount']['value']
                           for i in getHospitalRatingsAndCountQuery['results']['bindings']]
    result['ratingsLabel'] = hospitalRatingLabel
    result['ratingsCount'] = hospitalRatingCount
    return result

def get_rs_info(rs: str) -> Dict:
    GET_RS_INFO = (
        'SELECT * WHERE {'
        f'''
			  <{rs}>  :careEffectiveness ?care_effective ;
	              :careEffectivenessFootnote ?care_effective_fn ;
	              :careSafety ?care_safety ;
	              :careSafetyFootnote ?care_safety_fn ;
	              :careTimeliness ?care_timeliness ;
	              :careTimelinessFootnote ?care_timeliness_fn ;
	              :city ?city_uri ;
	              :county ?county_uri ;
	              :hasEmergencyServices ?has_emergency ;
	              :hasProviderID ?provider_id ;
	              :medicalImagingEfficientUse ?mi_efficiency ;
	              :medicalImagingEfficientUseFootnote ?mi_efficiency_fn ;
	              :meetsMeaningfulUseOfEHRs ?meaningful_ehr ;
	              :mortality ?mortality ;
	              :mortalityFootnote ?mortality_fn ;
	              :ownership ?ownership ;
	              :patientExperience ?patient_experience ;
	              :patientExperienceFootnote ?patient_experience_fn ;
	              :phoneNumber ?phone ;
	              :rating ?rating ;
	              :ratingFootnote ?rating_fn ;
	              :readmission ?readmission ;
	              :readmissionFootnote ?readmission_dn ;
	              :state ?state_uri ;
	              :type ?type ;
	              :zipCode ?zip_code ;
	        schema:address ?address ;
	          foaf:name ?name .
	  
          ?city_uri foaf:name ?city .
          ?county_uri foaf:name ?county .
          ?state_uri foaf:name ?state .
        '''
        '''
          OPTIONAL {
				    service <https://dbpedia.org/sparql> {
                ?county_uri dbo:country ?country .
            }	
				  }
        }
        ''')
    result = query(GET_RS_INFO)
    return result['results']['bindings']

def get_dbpedia_hospital():
	QUERY = '''
	SELECT distinct ?hospitalName {
  service <https://dbpedia.org/sparql> {
    ?hospital a dbo:Hospital .
    ?hospital dbo:state ?state .
    ?state dbo:country ?country .
    FILTER(?country IN(dbr:United_States))
	?hospital rdfs:label ?hospitalName .
	FILTER(lang(?hospitalName) = 'en')
  }
}
	'''
	getHospitalDBpedia = query(QUERY)
	resultRaw = [ i['hospitalName']['value'] for i in getHospitalDBpedia['results']['bindings'] ]
	result = [ i[:len(i) - 3] for i in resultRaw ]
	return result

def get_local_hospital():
	QUERY = '''
	SELECT distinct ?hospitalName 
	WHERE {
		?hospital a <http://dbpedia.org/resource/Hospital> .
		?hospital xsd:name ?hospitalName .
	}
	'''

	getHospitalLocal = query(QUERY)
	result = [ i['hospital']['value'] for i in getHospitalLocal['results']['bindings'] ]
	return result