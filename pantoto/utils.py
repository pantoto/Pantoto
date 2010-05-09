from django.template.defaultfilters import slugify

PERMISSIONS = (
           ("rw","Read-Write"),
           ("r-","Read-Only"),
           ("-w","Write-Only"),
           ("rn","Read-Restricted"),
           ("nw","Write-Restricted")
)

#Uncertain where this tuples should be or if it should be created 
#on the fly from the existing style information

THEME_TYPES = (
			("Blue","Misty Blue"),
			("Green","Yoda Green"),
			("Red","Ferrari Red")
)

def underscorify(txt):
    return slugify(txt).strip().replace('-','_')

def lookup_tuple(ltuple,lookupstr,code=True):
	lookupval = None	
	for eachperm in ltuple:
		if code:
			if lookupstr == eachperm[0]:
				lookupval = eachperm[1]
				break;
		else:
			if lookupstr == eachperm[1]:
				lookupval = eachperm[0]
	return lookupval



#================ HELP RELATED STUFF ============================
def get_helptext(objtype):
	helptext = ""
	if objtype == "user":
		helptext += "A User here is a User of the system. He / She can create Fields, Views (categories), author and edit Pagelets at a minimum. \
					Depending on the workflow and group that he / she is part of, the persmissions available on Pagelet fields change." 
	if objtype == "persona":
		helptext += "A Persona is assumed by a user during his / her session in Pantoto. Based on the persona the user assumes, his / her permissions on Paglet \
                    field get determined. This particularly helps in work flows where Personas (equivalent of Roles) can add / modify / delete / approve content \
                    during different stages of the work flow."
	if objtype == "field":
		helptext += "A Field is the atomic level of data in a Pagelet. Various authoring groups will have defined permissions on each field. \
					Permissions could be read-only / restricted write / read-write."
	if objtype == "viewCategory":
		helptext += "A ViewCategory (previously referred to as just Category) is a collective view of field that is closely tied to the state in the Work flow\
					that the Pagelet, which is being \"view\"ed, is in. For example an Application form in a view named \"Open\" may have editable fields, but\
					once the deadline is closed on the Applications, it assumes the merged field permissions of second view named \"Closed\" after which every \
					field becomes read-only."
	if objtype == "pagelet":
		helptext += "A pagelet is aggregation of fields. It is the core information blob of the Pantoto CMS. A pagelet can be viewed through the filters of \
					ViewCategories that get attached to the Pagelet that allow the user to control,manipulate and view the state of information in a Work flow."
	return helptext

