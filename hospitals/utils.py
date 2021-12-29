from typing import Dict
from pymantic import sparql

# TODO: set up env variables(Heroku env variables/?)
server = sparql.SPARQLServer(
    'http://169.254.0.72:9999/blazegraph/namespace/kb/sparql')

# Loading data to Blazegraph
server.update(
    'load <https://github.com/dnswd/semanthink/raw/main/hospital-ratings-rdf-5.ttl>')

prefixes = '''
	PREFIX : <http://example.org/>
	PREFIX schema: <http://schema.org/>
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
'''


def query(q):
    return server.query(prefixes + q)


def rs_res(res):
    return [r['rs']['value'] for r in res['results']['bindings']]


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
			SELECT ?rs
			WHERE {
				?rs a <http://dbpedia.org/resource/Hospital> .
				?rs foaf:name ?rsName .
				FILTER (regex(str(?rsName), "%s", "i"))
			} ORDER BY ?rs
		''' % rs
    return rs_res(query(GET_RS))


def get_rs_by_state(state):
    GET_STATE = '''
				SELECT ?rs
				WHERE {
					?rs :state ?state .
					?state foaf:name "%s" .
				} ORDER BY ?rs
			''' % state
    return rs_res(query(GET_STATE))


def get_rs_by_city(city):
    GET_CITY = '''
				SELECT ?rs
				WHERE {
					?rs :city ?city .
					?city foaf:name "%s" .
				} ORDER BY ?rs
			''' % city
    return rs_res(query(GET_CITY))


def get_rs_by_tipe(tipe):
    GET_TYPE = '''
				SELECT ?rs
				WHERE {
					?rs :type "%s" .
				} ORDER BY ?rs
			''' % tipe
    return rs_res(query(GET_TYPE))


def get_rs_by_ownership(ownership):
    GET_OWNERSHIP = '''
				SELECT ?rs
				WHERE {
					?rs :ownership "%s" .
				} ORDER BY ?rs
			''' % ownership
    return rs_res(query(GET_OWNERSHIP))


def get_rs_by_rating(rating):
    GET_RATING = '''
				SELECT ?rs
				WHERE {
					?rs :rating %s .
				} ORDER BY ?rs
			''' % rating
    return rs_res(query(GET_RATING))


def get_rs_by_emergency(emergency):
    GET_EMERGENCY = '''
				SELECT ?rs
				WHERE {
					?rs :hasEmergencyServices "%s" .
				} ORDER BY ?rs
			''' % emergency
    return rs_res(query(GET_EMERGENCY))


def get_rs_by_ehr(ehr):
	GET_EHR = '''
				SELECT ?rs
				WHERE {
					?rs :meetsMeaningfulUseOfEHRs "Y" .
				} ORDER BY ?rs
			'''
	return rs_res(query(GET_EHR))

def get_hospital_count():
	GET_HOSPITAL_COUNT = 	'''
		SELECT (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
		}
	'''
	hospitalCountQuery = query(GET_HOSPITAL_COUNT)
	return int(hospitalCountQuery['results']['bindings'][0]['hospitalCount']['value'])

def get_er_count():
	GET_ER_COUNT = 	'''
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
	GET_PATIENT_EXPERIENCES_AND_COUNT = 	'''
		SELECT ?patientRating (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
			?hospital :patientExperience ?patientRating .
		} GROUP BY ?patientRating
	'''
	getPatientExperiencesAndCountQuery = query(GET_PATIENT_EXPERIENCES_AND_COUNT)
	result = {}
	patientExperinceLabel = [ i['patientRating']['value'] for i in getPatientExperiencesAndCountQuery['results']['bindings'] ]
	patientExperienceCount = [ i['hospitalCount']['value'] for i in getPatientExperiencesAndCountQuery['results']['bindings'] ]
	result['experienceLabel'] = patientExperinceLabel
	result['experienceCount'] = patientExperienceCount
	return result

def get_hospital_overall_rating_and_count():
	GET_HOSTPITAL_OVERALL_RATING_AND_COUNT = 	'''
		SELECT ?rating (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
			?hospital :rating ?rating .
		} GROUP BY ?rating
	'''
	getHospitalRatingsAndCountQuery = query(GET_HOSTPITAL_OVERALL_RATING_AND_COUNT)
	result = {}
	hospitalRatingLabel = [ i['rating']['value'] for i in getHospitalRatingsAndCountQuery['results']['bindings'] ]
	hospitalRatingCount = [ i['hospitalCount']['value'] for i in getHospitalRatingsAndCountQuery['results']['bindings'] ]
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
        '}')
    result = query(GET_RS_INFO)
    return result['results']['bindings']
