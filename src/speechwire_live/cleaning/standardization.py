"""
Uses:
    School Info.xlsx
"""

#Add in a rule of "If string starts with 'Mc', capitalize 3rd letter (McCormick, McKnight, etc.)
import pandas as pd
class Standardizer:
    def __init__(self):
        # Define dictionaries for each type of standardization
        self.event_names = {
            "DI":"DI","HI":"HI","DUO":"DUO","OID":"OID","POE":"POE","POI":"POI","OO":"OO","INF":"INF","ENT":"ENT","EXT":"EXT","IMP":"IMP","Duet":"Duet",
            'Dramatic Interpretation':'DI','Oral Interpretation of Serious Prose':'DI','Dramatic Interp':'DI', 'Varsity Dramatic Interpretation':'DI', 'Varsity Oral Interpretation of Serious Prose':'DI',
            'Humorous Interpretation':'HI','Oral Interpretation of Humorous Prose':'HI','Humorous Interp':'HI', "Humorous Interpretaion":"HI",'Varsity Humorous Interpretation':'HI', "Humorous Interpretaion":"HI", 'Humourous Interpretation':'HI', 'HUMOR':'HI', 'Varsity Oral Interpretation of Humorous Prose':'HI',
            'Poetry':'POE', 'Oral Interpretation of Poetry':'POE','Poetry Interpretation':'POE', "Poetry Interp":"POE", 'Varsity Oral Interpretation of Poetry':'POE',
            'Program Oral Interp':'POI','Program of Oral Interp.':'POI','Program Oral Interpretation':"POI",'Program of Oral Interpretation':'POI','Program of Interpretation':'POI', 'Varsity Program Oral Interpretation':'POI', 'Varsity POI':'POI',
            'Duo Interpretation':'DUO','Duo':'DUO','Duet Acting':'DUO',"Duo/Duet Interpretation":"DUO",'Duo Interp':'DUO','Duet Acting/Duo Interp':'DUO', 'Varsity Duo Interpretation':'DUO', 'DUO Interp':'DUO', #'Duo Interpretation ':'DUO',
            'Oral Interpretation of Drama':'OID',
            'Original Oratory':'OO','Persuasive Speaking':'OO','Persuasive':'OO', "Oratory":"OO", 'Varsity Persuasive Speaking':'OO', 'Oratory':'OO', 'Varsity Original Oratory':'OO',
            'Informative Speaking':'INF','Informative':'INF', 'Varsity Informative Speaking':'INF', 'Varsity Informative':'INF', 'Inform':'INF', 'INFO':'INF',
            'Entertainment Speaking':'ENT','Entertainment':'ENT', 
            'Extemporaneous Speaking':'EXT', 'Extemporaneous':'EXT','Extemp':'EXT', "Extemp Speaking":"EXT",  'Combined Extemp':'EXT', 'EXTEMP':'EXT', 'Domestic Extemp':'EXT', 'International Extemp':'EXT', 'Combined Extemporaneous':'EXT', 'Varsity Extemporaneous Speaking':'EXT', 'US Extemp':"EXT",
            'Impromptu Speaking':'IMP','Impromptu':'IMP', 'Varsity Impromptu':'IMP',          
            
            'A-2 Duo Interpretation':'DUO', 'A-2 Entertainment Speaking':'ENT', 'A-2 Extemporaneous Speaking':'EXT', 'A-2 Informative Speaking':'INF', 'A-2 Oral Interpretation of Drama':'OID', 'A-2 Oral Interpretation of Humorous Prose':'HI', 'A-2 Oral Interpretation of Poetry':'POE', 'A-2 Oral Interpretation of Serious Prose':'DI', 'A-2 Persuasive Speaking':'OO', 'A-2 Program Oral Interpretation':'POI',
            'A-3 Duo Interpretation':'DUO', 'A-3 Entertainment Speaking':'ENT', 'A-3 Extemporaneous Speaking':'EXT', 'A-3 Informative Speaking':'INF', 'A-3 Oral Interpretation of Drama':'OID', 'A-3 Oral Interpretation of Humorous Prose':'HI', 'A-3 Oral Interpretation of Poetry':'POE', 'A-3 Oral Interpretation of Serious Prose':'DI', 'A-3 Persuasive Speaking':'OO', 'A-3 Program Oral Interpretation':'POI',

        }
        
        self.event_names_during_tournaments = {
            "DI":"DI","HI":"HI","DUO":"DUO","OID":"OID","POE":"POE","POI":"POI","OO":"OO","INF":"INF","ENT":"ENT","EXT":"EXT","IMP":"IMP","Duet":"Duet",
            'Dramatic Interpretation':'DI','Oral Interpretation of Serious Prose':'DI','Dramatic Interp':'DI', 'Novice Dramatic Interpretation':'N-DI', 'Varsity Dramatic Interpretation':'DI', 'Varsity Oral Interpretation of Serious Prose':'DI',
            'Humorous Interpretation':'HI','Oral Interpretation of Humorous Prose':'HI','Humorous Interp':'HI', 'Novice Humorous Interpretation':'N-HI', 'Varsity Humorous Interpretation':'HI', "Humorous Interpretaion":"HI", 'Novice Humorous Interpretaion':'N-HI', 'Humourous Interpretation':'HI','HUMOR':'HI', 'Varsity Oral Interpretation of Humorous Prose':'HI',
            'Poetry':'POE', 'Oral Interpretation of Poetry':'POE','Poetry Interpretation':'POE', 'Novice Oral Interpretation of Poetry':'N-POE', 'Varsity Oral Interpretation of Poetry':'POE', 'Novice Poetry Interp':'N-POE',
            'Program Oral Interp':'POI','Program of Oral Interp.':'POI','Program Oral Interpretation':"POI",'Program of Oral Interpretation':'POI','Program of Interpretation':'POI', 'Varsity Program Oral Interpretation':'POI', 'Varsity POI':'POI',
            'Duo Interpretation':'DUO','Duo':'DUO','Duet Acting':'DUO',"Duo/Duet Interpretation":"DUO",'Duo Interp':'DUO','Duet Acting/Duo Interp':'DUO',  'Varsity Duo Interpretation':'DUO', 'DUO Interp':'DUO',
            'Oral Interpretation of Drama':'OID',
            'Original Oratory':'OO','Persuasive Speaking':'OO','Persuasive':'OO', 'Novice Persuasive Speaking':'N-OO', 'Varsity Persuasive Speaking':'OO', 'Novice Oratory':'N-OO', 'Oratory':'OO','Novice Original Oratory':'N-OO', 'Varsity Original Oratory':'OO',
            'Informative Speaking':'INF','Informative':'INF', 'Varsity Informative Speaking':'INF', 'Novice Informative Speaking':'N-INF', 'Varsity Informative':'INF','Inform':'INF', 'INFO':'INF',
            'Entertainment Speaking':'ENT','Entertainment':'ENT',  'Varsity Entertainment':'ENT', 'Novice Entertainment Speaking':'N-ENT','Varsity Entertainment Speaking':'ENT',
            'Extemporaneous Speaking':'EXT', 'Extemporaneous':'EXT','Extemp':'EXT','Novice Extemporaneous Speaking':'N-EXT', 'Varsity Extemporaneous Speaking':'EXT', "Extemp Speaking":"EXT", 'Novice Extemp Speaking':'N-EXT', 'Combined Extemp':'EXT', 'EXTEMP':'EXT', "US Extemp":"EXT",
            'Impromptu Speaking':'IMP','Impromptu':'IMP', 'Varsity Impromptu':'IMP',
           
            'A-2 Duo Interpretation':'DUO', 'A-2 Entertainment Speaking':'ENT', 'A-2 Extemporaneous Speaking':'EXT', 'A-2 Informative Speaking':'INF', 'A-2 Oral Interpretation of Drama':'OID', 'A-2 Oral Interpretation of Humorous Prose':'HI', 'A-2 Oral Interpretation of Poetry':'POE', 'A-2 Oral Interpretation of Serious Prose':'DI', 'A-2 Persuasive Speaking':'OO', 'A-2 Program Oral Interpretation':'POI',
            'A-3 Duo Interpretation':'DUO', 'A-3 Entertainment Speaking':'ENT', 'A-3 Extemporaneous Speaking':'EXT', 'A-3 Informative Speaking':'INF', 'A-3 Oral Interpretation of Drama':'OID', 'A-3 Oral Interpretation of Humorous Prose':'HI', 'A-3 Oral Interpretation of Poetry':'POE', 'A-3 Oral Interpretation of Serious Prose':'DI', 'A-3 Persuasive Speaking':'OO', 'A-3 Program Oral Interpretation':'POI',
            
        }
        
        self.school_names = {
            #Millard Schools
            'Millard North':'MN','MIllard North':'MN', 
            'Millard West':'MW','Millard South':'MS',
            #Bellevue Schools
            'Bellevue West':'BW','Bellevue East':'BE',
            #Papillion Schools
            'Papillion-LaVista':'PLVH', 'Papillion-LaVista South':'PLVS',
            #Gretna Schools
            'Gretna High School':'G','Gretna':'G',
            'Gretna East':'GE','Gretna East High School':'GE',
        
            #Lincoln Schools
            'Lincoln East':'LE',
            'Lincoln Southwest':'LSW', 'Lincon Southwest':'LSW',
            'Lincoln Southeast':'LSE','Lincoln Southeast Speech':'LSE',
            'Lincoln Northeast':'LNE',
            'Lincoln North West':'LNW','Lincoln Northwest':'LNW',
            'Lincoln North Star Speech':'LNS','Lincoln North Star':'LNS',
            'Lincoln High':'LH','Lincoln High Speech':'LH', 'Lincoln High School':'LH',
            'Lincoln Pius X':'Pius X', 'Pius X':'Pius X',
            'Lincoln Standing Bear':'LSB',
            'The LNK':'LNK', 'LNK':'LNK',
            'Lincoln Lutheran':'LL',
            #Elkhorn Schools
            'Elkhorn High School':'EHS', 'Elkhorn High':'EHS',
            'Elkhorn North':'ENHS','Elkhorn North High School':'ENHS', 'Elkhorn North High School Speech Team':'ENHS',
            'Elkhorn South':'ESHS','Elkhorn South High School':'ESHS','Elkhorn South Speech':'ESHS',
            #OPS Schools
            'Omaha Central high School':'OCHS','Omaha Central':'OCHS','Omaha Central High School':'OCHS',
            'Omaha North':'ONHS','Omaha North High School':'ONHS','Omaha North Speech':'ONHS',
            'Omaha South':'OSHS',
            'Omaha Westview':'OWHS', 'Westview Wolverine Speech and Debate':'OWHS',
            'Omaha Northwest High School':'ONWH', 'Omaha Northwest':'ONWH',
            'Omaha Buena Vista High School':'OBVH','Omaha Buena Vista':'OBVH',
            'Omaha Bryan High School':'OBry','Omaha Bryan':'OBry','Bryan High School':'OBry',
            'Omaha Burke High School':'OBur','Omaha Burke':'OBur','Burke High School':'OBur','Burke':'OBur',
            'Omaha Benson':'OBen','Omaha Benson High School':'OBen',
            'Westside':'Westside',
            #Omaha Catholic Schools
            'Omaha Skutt Catholic':'Skutt',
            'Duchesne':'Duch','Omaha Duchesne Academy':'Duch', 'Omaha Duchense Academy':'Duch',
            'Creighton Prep':'Prep', 'Creighton Prep':'Prep',
            'Marian':'Marian',
            'Brownell-Talbot':'BT', 'Omaha Brownell-Talbot':'BT', 'Omaha Brownell Talbot':'BT',
            'Elkhorn Mount Michael':'MM',
            'Mercy High School':'Mercy',

            #Yet to be categorized
            'Norfolk Senior H.S.':'Norf',
            'Norris High School':'Norr', 'Norris':'Norr',
            'Douglas County West':'DCW', 'DC West':'DCW',
            'Raymond Central':'RC',
            'Fremont High School':'Fre',
            'Grand Island':'GI','Grand Island Speech':'GI',
            'Bennington':'Benn',
            'Hastings':'Hast','Hastings Senior High':'Hast',
            'Kearney':'Kear',
            'North Platte':'NorP',
            'Lexington':'Lex',
            'Beatrice Speech':'Beat','Beatrice':'Beat',
            'Blair High School Speech Team':'Blair','Blair':'Blair',
            'Nebraska City High School Speech':'NebC', 'Nebraska City':'NebC',
            'Crete High School':'Crete', 'Crete':'Crete',
            'Wisner-Pilger':'WisP',
            'Fairbury':'Fairb',
            'Ashland-Greenwood':'A-G',
            'Plattsmouth High School':'Plattsmouth',
            'Schuyler Central High School':'Schuy Central',
            
            'Waverly High School':'Wav',
            'Waukee Northwest':'WNW',
            'Scotus Central Catholic':'Scotus',
            'Platteview High School':'Platteview',
            'South Sioux City':'S Sioux',
            'Columbus Lakeview':'Col Lakeview',
            'Wahoo-Bishop Neumann':'WBN',
            'Scottsbluff High School':'Scottsbluff',
            'David City':'DvC',
            'York':'York',
            'Malcolm':'Malc',
            'Milford High School':'Milf',
            'Elmwood Murdock Schools':'Elm. Murd.',
            'Auburn High School':'Aub',
            'Aquinas Catholic':'AqCa',
            'Kenesaw':'Kenesaw',
            'Parkview Christian':'PkvC',
            'Concordia':'Conc',
            'Conestoga':'Cnstog',
            'Tri Country':'TriC',
            'Falls City High School':'Falls City',
            'Humboldt Table Rock Steinauer':'HTRS',
            
            'Columbus H.S.':'Columbus',
            'West Central':'WC',
            'Lourdes Central Catholic':'LCC',
            'Palmyra High School':'Palmyra',
            'Lewiston Schools':'Lewiston',
            'Sioux City East High School Speech':'Sioux City East',
            'Tea Area':'TA',
            'Tripp-Delmont':'T-D',
            'Nebraska Lutheran':'Neb Luth',
            'Archbishop Bergan':'Arch Berg',
            
            'Sioux Falls Washington':'*SxFW', 'Washington HS Interp':'*SxFW',
            'Sioux Falls Christian':'*SxFC',
            'SF Lincoln':'*SxFL', 'SF Lincoln High School':'*SxFL',
            'SF Roosevelt':'*SxFR',
            'Sioux Falls Jefferson':'*SxFJ',
            'Siouxland Christian School':'*SxC', 'Siouxland Christian':'*SxC',
            'Atlantic High School':'*Atl',
            'Brandon Valley High School':'*BV', 'Brandon Valley':'*BV', 'BrandonValley':'*BV',
            'Roosevelt High School':'*Rsvlt',
            "O'Gorman":'*OG',"O'Gorman High School":"*OG",
            'Jefferson High School':'*JHS',
            'Dakota Valley':'*DV',
        }
        
        self.tournament_order = {
            '25-26': {
                'OBVH':1, 'PLVS':2, 'MS':3, 'Pius X':4, 'Norris':5, 'LH':6, 'PLVH':7, 'LSE':8,
                'Fre':9, 'GE':10, 'RC':11, 'SFL':12, 'EHS':13, 'LSW':14, 'LNE':15, 'MW':16,
                'BW':17, 'LNS':18, 'Marian':19, 'MN':20, 'LE':21, 
                'NQ_N':22, 'NQ_N DX':23, 'NQ_S':24, 'NQ_S DX':25, 
                'A1':26, 'A2':27, 'A3':28, 'A4':29,
            },
            
            '25-26/Novice': {
                'MN Novice':1, 'MW GOLD':2, 'PLVS':3, 'Pius X':4, 'Bryan GOLD':5, 'LH':6,
                'MS GOLD':7, '__ GOLD':8,
            },
            
            '24-25': {
                'PLVS':1, 'OBVH':2, 'MS':3, 'Pius X':4, 'LNK':5,
                'Norr':6, 'LH':7, 'LSE':8,
                'Fre':9, 'EHS':10, 'LSW':11, 'LNE':12, 'MW':13,
                'BW':14, 'LNS':15, 'Marian':16, 'MN':17, 'LE':18,
                'NQ_N':19, 'NQ_S':20, 'A1':21, 'A2':22, 'A3':23, 'A4':24,          
            },
            
            '23-24':{
                'BW':1,'PLVH':2,'MS':3,'Pius X':4,
                'Norr':5,'PLVS':6,'LH':7,'Creighton Prep':8,'LSE':9,
                'Doane':10,'Westside':11,'RC':12,'EHS':13,'LSW':14,'LNE':15,'MW':16,
                'LNS':17,'Marian':18,'MN':19,'LE':20,'NQ_N':21,'NQ_S':22,'A1':23,'A4':24,
            },
        }
        
        self.judge_names = {
            'Chloe Meier':'C Meier-Bates', 'C Meier':'C Meier-Bates', 'C Meier Bates':'C Meier-Bates', 'C Meier-Bates':'C Meier-Bates','C. Meier-Bates':'C Meier-Bates',
            'Ben Leathers-Arnold':'Benjamin Leathers-Arnold',
            'Phil Pader':'Phil Paider',
            'Matt Jackson':'Matthew Jakson','Matthew Jakson':'Matthew Jackson',
            'Madison Placke (Glause)':'Madison Placke', 'Madison Glause':'Madison Placke',
            'Lizzy Janssen':'Lizzy Jansen',
            'JaeLeigh’s Askew':'JaeLeigh Askew', 'Jaeleigh Askew':'JaeLeigh Askew',
            'Gracelyn Baker':'Gracie Baker',
            'Kenzie Carlson':'McKenzie Carlson',
            'Sophia Dwyer':'Sophee Dwyer',
            'Adyen Johnson':'Ayden Johnson',
            'Emma Jorgeson':'Emma Jorgenson',
            'Hallie Nicholson':'Hailie Nicholson',
            'Emily Glinsman':'Emily Glinsmann',
            'Taylor Peterson':'Taylor Petersen',
            'Ethan Carslon':'Ethan Carlson',
            'George Grinell':'George Grinnell',
            'Rachel Vanengen':'Rachel VanEngen',
            'Ben Morgan':'Benjamin Morgan',
            'Maddie Stoerp':'Madeline Stoerp',
            'Lilly Frields':'Lillian Frields',
            'Char Olberding':'Charlotte Olberding',
            'Esman Rodas':'Esman Rodas Calderon',
            'Travis Grafe':'Travis Grafe-Cline',
            'Shreeya Shapokota':'Shreeya Shapkota', 
            'Chloe Fiscaro':'Chloe Fisicaro',
        }
        
        self.competitor_names = {
            'Anita Mashayekhia':'Anita Mashayekhi',
            'Sophia Naber':'Corey Naber',
            'Sophie Bathel':'Sophia Bathel',
            'Vinnie Plasek':'Vixen Plasek','Vinnie Plasek, Zachary Wellman':'Vixen Plasek, Zachary Wellman',
            'Ben Pelzer':'Benjamin Pelzer','Benjamin R. Pelzer':'Benjamin Pelzer','Benjamin R. Pelzer, Zach Brown':'Benjamin Pelzer, Zach Brown',
            'Adrien Antunez':'Adrian Antunez',
            'Jake Sopscich':'Jake Sopsich',
            'Lilly Leathers':'Lily Leathers',
            'Kami Krecje':'Kami Krejce',
            
            'Abhiran Syamala':'Abhiram Syamala',
            'Amelia Schupach':'Amelia Schupbach',
            'Apollp Zephier':'Apollo Zephier',
            'Claire Timperly':'Claire Timperley',
            'Mahid Farahmand':'Mahshid Farahmand', 'Mahshid Faramand':'Mahshid Farahmand',
            'Megha Moorthy':'Meghna Moorthy',
            'Prajwal Saji':'Prajwal Rao Sagi',
            'Sahasra Madungundu':'Sahasra Madugundu',
            'violet Christen':'Violet Christen',
            'alej Manyiel':'Alej Manyiel',
            'Isiaah Rahman, Seth Umphreys':'Isaiah Rahman, Seth Umphreys', 'Isiaah Rahman':'Isaiah Rahman',
        }
        
        self.millard_north_names = {
            'Sophia Naber':'Corey Naber',
            'Kennedy Mcknight':'Kennedy McKnight',
            'Gabrielle Burns':'Gabby Burns',
            'Cecelia Vlieger':'Cece Vlieger',
            'Katy Mckinley':'Katy McKinley',
            'Mckinley Toft':'McKinley Toft',
            'Mckenzie Schwarz':'McKenzie Schwarz',
            'Laurel Mccall':'Laurel McCall',
        }
        
        self.oid_names = {
            #Bennington 1
            'Addison Yates, Grace Hoffmann, Jack Holtorf, Liam Doan, Natalie Rivera':'Grace Hoffmann, Liam Doan, Natalie Rivera, Addison Yates/Jack Holtorf/Katherine Sukraw', 'Addison Yates, Grace Hoffmann, Katherine Sukraw, Liam Doan, Natalie Rivera':'Grace Hoffmann, Liam Doan, Natalie Rivera, Addison Yates/Jack Holtorf/Katherine Sukraw', 'Grace Hoffmann, Jack Holtorf, Katherine Sukraw, Liam Doan, Natalie Rivera':'Grace Hoffmann, Liam Doan, Natalie Rivera, Addison Yates/Jack Holtorf/Katherine Sukraw',
            #Bennington 2
            'Alice Hofer, Desi Coles, Henry Houska, Jay Kruse':'Alice Hofer, Desi Coles, Henry Houska, Jay Kruse, (Prise Yates)', 'Alice Hofer, Desi Coles, Henry Houska, Jay Kruse, Prise Yates':'Alice Hofer, Desi Coles, Henry Houska, Jay Kruse, (Prise Yates)',
            #EHS
            'Chase Engel, Evan Carlson, Noelle Dutoit, Oliver Raiser, Quinton Raiser':'Chase Engel, Evan Carlson, Noelle Dutoit, Quinton Raiser, Oliver Raiser/Samantha Richards', 'Chase Engel, Evan Carlson, Noelle Dutoit, Quinton Raiser, Samantha Richards':'Chase Engel, Evan Carlson, Noelle Dutoit, Quinton Raiser, Oliver Raiser/Samantha Richards',
            #Beatrice 1
            'Isaiah York, Jenae Farley, Kadence Clark, Killian Killough, Shelby Eldridge':'Jenae Farley, Kadence Clark, Killian Killough, Shelby Eldridge, Brayton Rogge/Isaiah York', 'Brayton Rogge, Jenae Farley, Kadence Clark, Killian Killough, Shelby Eldridge':'Jenae Farley, Kadence Clark, Killian Killough, Shelby Eldridge, Brayton Rogge/Isaiah York',
            #Beatrice 2 (Krecje should be Krejce, no members change)
            'Elizabeth Wallace, Jennifer Hare, Kami Krecje, Violet Basargin':'Elizabeth Wallace, Jennifer Hare, Kami Krejce, Violet Basargin',
            #ENHS 
            'Chloe Holmquist, Ellie Duan, Lincoln Petrick, Zack Anderson, Zen Wesselmann':'Chloe Holmquist, Junya (Ellie) Duan, Lincoln Petrick, Zack Anderson, Zen Wesselmann',
            #LNS
            'Addi Nolte, Lauren Hellbusch, Reyce Usher, Rylee Lieske, Styx Stuart':'Addi Nolte, Lauren Hellbusch, Reyce Usher, Rylee Lieske, Styx Stuart/Taylor Price', 'Addi Nolte, Lauren Hellbusch, Reyce Usher, Rylee Lieske, Taylor Price':'Addi Nolte, Lauren Hellbusch, Reyce Usher, Rylee Lieske, Styx Stuart/Taylor Price',
            #Creighton Prep
            'Anthony Wellwood, Brennen Nelson, Chris Tollo, Ethan Schroeder, Will Tabor':'Anthony Wellwood, Will Tabor, Chris Tollo/Ed Watson/Joseph Marar, Ethan Schroeder/Brennen Nelson', 'Anthony Wellwood, Chris Tollo, Ed Watson, Joseph Marar, Will Tabor':'Anthony Wellwood, Will Tabor, Chris Tollo/Ed Watson/Joseph Marar, Ethan Schroeder/Brennen Nelson', 'Anthony Wellwood, Ed Watson, Ethan Schroeder, Joseph Marar, Will Tabor':'Anthony Wellwood, Will Tabor, Chris Tollo/Ed Watson/Joseph Marar, Ethan Schroeder/Brennen Nelson',
            #Plattsmouth
            'Connor Haberman, Jaxon Sharp, Jeffrey Meisinger, Lucy Alldredge, Sophia Alldredge':'Jaxon Sharp, Jeffrey Meisinger, Lucy Alldredge, Sophia Alldredge, Connor Haberman/Nathan Zak', 'Jaxon Sharp, Jeffrey Meisinger, Lucy Alldredge, Nathan Zak, Sophia Alldredge':'Jaxon Sharp, Jeffrey Meisinger, Lucy Alldredge, Sophia Alldredge, Connor Haberman/Nathan Zak',
            #North Platte
            'Finnley Eickhoff, Isabella Frazier, Katelynn Mcneel, Tuesday Allen, Xaivria Lemmer':'Finnley Eickhoff, Isabella Frazier, Tuesday Allen, Xaivria Lemmer, Katelynn Mcneel/Marisa Pfeifer', 'Finnley Eickhoff, Isabella Frazier, Marisa Pfeifer, Tuesday Allen, Xaivria Lemmer':'Finnley Eickhoff, Isabella Frazier, Tuesday Allen, Xaivria Lemmer, Katelynn Mcneel/Marisa Pfeifer',
            #Skutt
            'Abigail Sommer, Catherine Youell, Eric Weaver, Kate Wester, Nola Herfordt':'Abigail Sommer, Catherine Youell, Kate Wester, Nola Herfordt, Josh Zaleski/Eric Weaver', 'Abigail Sommer, Catherine Youell, Josh Zaleski, Kate Wester, Nola Herfordt':'Abigail Sommer, Catherine Youell, Kate Wester, Nola Herfordt, Josh Zaleski/Eric Weaver',
            #LSE
            'Aj Lempke, Phoenix Braatz, Timber Wooledge':'Phoenix Braatz, Timber Wooledge, Aj Lempke/Madeline Jensen', 'Madeline Jensen, Phoenix Braatz, Timber Wooledge':'Phoenix Braatz, Timber Wooledge, Aj Lempke/Madeline Jensen',
        
        #25-26
            #Auburn 1
            'Alexa Janssen, Beau Thomas, Charlotte Dickerson, Ella Ackley, Kinsley Gerdes':'Beau Thomas, Ella Ackley, Kinsley Gerdes, Alexa Janssen/Charlotte Dickerson/Gillian Hanna', 'Alexa Janssen, Beau Thomas, Ella Ackley, Gillian Hanna, Kinsley Gerdes':'Beau Thomas, Ella Ackley, Kinsley Gerdes, Alexa Janssen/Charlotte Dickerson/Gillian Hanna', 'Beau Thomas, Charlotte Dickerson, Ella Ackley, Gillian Hanna, Kinsley Gerdes':'Beau Thomas, Ella Ackley, Kinsley Gerdes, Alexa Janssen/Charlotte Dickerson/Gillian Hanna',
            #Auburn 2
            'Colt Zentner, Elijah Powell, Hunter Stevenson, Kyle Jones, Solomon Jacobitz':'Elijah Powell, Hunter Stevenson, Kyle Jones, Solomon Jacobitz, Colt Zentner/Ian Mather', 'Elijah Powell, Hunter Stevenson, Ian Mather, Kyle Jones, Solomon Jacobitz':'Elijah Powell, Hunter Stevenson, Kyle Jones, Solomon Jacobitz, Colt Zentner/Ian Mather',
            #Beatrice
            'Isabelle Parsons, Jenae Farley, Juniper Kaufman, Violet Basargin, Moonshine Kaufman':'Isabelle Parsons, Jenae Farley,  Violet Basargin, Moonshine Kaufman, Juniper Kaufman/Khloe Okeefe',
            'Isabelle Parsons, Jenae Farley, Khloe Okeefe, Violet Basargin, Moonshine Kaufman':'Isabelle Parsons, Jenae Farley,  Violet Basargin, Moonshine Kaufman, Juniper Kaufman/Khloe Okeefe',
            #Bennington
            'Cormac Eckholt, Dominique Bisselou, Grayson Reed, Katie Miller, Natalie Rivera':'Cormac Eckholt, Grayson Reed, Katie Miller, Natalie Rivera, Grace Hoffmann/Dominique Bisselou',
            'Cormac Eckholt, Grace Hoffmann, Grayson Reed, Katie Miller, Natalie Rivera':'Cormac Eckholt, Grayson Reed, Katie Miller, Natalie Rivera, Grace Hoffmann/Dominique Bisselou',
            #DC West
            'Addison Klawitter, Benji Oien, Jaxon Swierczek, Joslyn Giles, Nylee Hayner':'Benji Oien, Jaxon Swierczek, Joslyn Giles, Nylee Hayner, Addison Klawitter/Noelle Beyl',
            'Benji Oien, Jaxon Swierczek, Joslyn Giles, Noelle Beyl, Nylee Hayner':'Benji Oien, Jaxon Swierczek, Joslyn Giles, Nylee Hayner, Addison Klawitter/Noelle Beyl',
            #David City
            'Brittin Valentine, Ellie Bales, Madie Summers, Paul Tebbe, Trevin Jahde':'Brittin Valentine, Ellie Bales, Madie Summers, Paul Tebbe, Trevin Jahde',
            'Brittin Valentine, Ellie Bales, Madie Summers, Trevin Jahde':'Brittin Valentine, Ellie Bales, Madie Summers, Paul Tebbe, Trevin Jahde',
            #Elkhorn North
            'Chloe Holmquist, Junya (Ellie) Duan, Lincoln Petrick, Zack Anderson, Zen Wesselmann':'Junya (Ellie) Duan, Lincoln Petrick, Zack Anderson, Zen Wesselmann, Chloe Holmquist/Morgan Lavin',
            'Junya (Ellie) Duan, Lincoln Petrick, Morgan Lavin, Zack Anderson, Zen Wesselmann':'Junya (Ellie) Duan, Lincoln Petrick, Zack Anderson, Zen Wesselmann, Chloe Holmquist/Morgan Lavin',
            #Lincoln North Star
            'Addi Nolte, Daisy Marshall, Kaylee Brhel':'Addi Nolte, Daisy Marshall, Oliver Shively, Skylar Kaspar, Kaylee Brhel/Anteya Gesch',
            'Addi Nolte, Daisy Marshall, Kaylee Brhel, Oliver Shively, Skylar Kaspar':'Addi Nolte, Daisy Marshall, Oliver Shively, Skylar Kaspar, Kaylee Brhel/Anteya Gesch',
            'Addi Nolte, Anteya Gesch, Daisy Marshall, Oliver Shively, Skylar Kaspar':'Addi Nolte, Daisy Marshall, Oliver Shively, Skylar Kaspar, Kaylee Brhel/Anteya Gesch',
            #Lincoln Southeast (?)
            'Beau Cassell, Braxton Wiebke, Jordyn Rizza, Padraig Fargen':'Beau Cassell, Jordyn Rizza, Padraig Fargen/Braxton Wiebke/Sophia Winkler',
            'Beau Cassell, Jordyn Rizza, Leann Braatz, Sophia Winkler':'Beau Cassell, Jordyn Rizza, Padraig Fargen/Braxton Wiebke/Sophia Winkler',
            'Beau Cassell, Jordyn Rizza, Padraig Fargen, Sophia Winkler':'Beau Cassell, Jordyn Rizza, Padraig Fargen/Braxton Wiebke/Sophia Winkler',
            #Malcolm
            'Bella Bostock, Erinna Ferguson, Grant Lewis, Harrison Paider, Julia Wolfe':'Grant Lewis, Harrison Paider, Julia Wolfe, Bella Bostock/Erinna Ferguson/Kami Kremer',
            'Bella Bostock, Grant Lewis, Harrison Paider, Julia Wolfe, Kami Kremer':'Grant Lewis, Harrison Paider, Julia Wolfe, Bella Bostock/Erinna Ferguson/Kami Kremer',
            'Erinna Ferguson, Grant Lewis, Harrison Paider, Julia Wolfe, Kami Kremer':'Grant Lewis, Harrison Paider, Julia Wolfe, Bella Bostock/Erinna Ferguson/Kami Kremer',
        
        }
                
    def standardize_event_name(self,name):
        """Standardizes an event name."""
        return self.event_names.get(name,name)
    
    def standardize_event_name_during_tournament(self,name):
        """Standardizes an event name during tournaments."""
        return self.event_names_during_tournaments.get(name,name)
    
    def standardize_school_name(self, name):
        """Standardizes a school name."""
        return self.school_names.get(name, name)
    
    def standardize_judge_name(self, name):
        """Standardizes a judge's name."""
        return self.judge_names.get(name, name)
    
    def standardize_competitor_name(self, name):
        """Standardizes a competitor's name."""
        return self.competitor_names.get(name, name)
    
    def standardize_millard_north_name(self, name):
        """Standardizes a Millard North competitor's name."""
        return self.millard_north_names.get(name, name)

    def standardize_oid_name(self, name):
        """Standardizes an OID name."""
        return self.oid_names.get(name, name)

    def get_tournament_order_index(self, name, year):
        """Returns the numerical index of a tournament name."""
        return self.tournament_order[year].get(name, name)
    
    def get_tournament_order_list(self, year):
        return list(self.tournament_order[year].keys())

    def get_district_or_class_dict(self, class_or_district, year):
        path = f"C:/Users/noahj/Desktop/Forensics/{year}/School Info.xlsx"
        df = pd.read_excel(path)
        df.index = df['School'] #Sets df's index as school abbreviations
        
        return df.to_dict()[f'{class_or_district}']
            
# %%
# def Standardize_SchoolNames():
#     Replacements = {#Millard Schools
#                     'Millard North':'MN', 'Millard West':'MW','Millard South':'MS',
#                     #Bellevue Schools
#                     'Bellevue West':'BW','Bellevue East':'BE',
#                     #Papillion Schools
#                     'Papillion-LaVista':'PLVH', 'Papillion-LaVista South':'PLVS',
#                     #Gretna Schools
#                     'Gretna High School':'G','Gretna':'G',
#                     'Gretna East':'GE','Gretna East High School':'GE',
                
#                     #Lincoln Schools
#                     'Lincoln East':'LE',
#                     'Lincoln Southwest':'LSW',
#                     'Lincoln Southeast':'LSE','Lincoln Southeast Speech':'LSE',
#                     'Lincoln Northeast':'LNE',
#                     'Lincoln North West':'LNW','Lincoln Northwest':'LNW',
#                     'Lincoln North Star Speech':'LNS','Lincoln North Star':'LNS',
#                     'Lincoln High':'LH','Lincoln High Speech':'LH', 
#                     'Lincoln Pius X':'Pius X', 'Pius X':'Pius X',
#                     'Lincoln Standing Bear':'LSB',
#                     'The LNK':'LNK', 'LNK':'LNK',
#                     #Elkhorn Schools
#                     'Elkhorn High School':'EHS',
#                     'Elkhorn North':'ENHS','Elkhorn North High School':'ENHS',
#                     'Elkhorn South':'ESHS','Elkhorn South High School':'ESHS','Elkhorn South Speech':'ESHS',
#                     #OPS Schools
#                     'Omaha Central high School':'OCHS','Omaha Central':'OCHS','Omaha Central High School':'OCHS',
#                     'Omaha North':'ONHS','Omaha North High School':'ONHS','Omaha North Speech':'ONHS',
#                     'Omaha South':'OSHS',
#                     'Omaha Westview':'OWHS',
#                     'Omaha Northwest High School':'ONWH', 'Omaha Northwest':'ONWH',
#                     'Omaha Buena Vista High School':'OBVH','Omaha Buena Vista':'OBVH',
#                     'Omaha Bryan High School':'OBry','Omaha Bryan':'OBry','Bryan High School':'OBry',
#                     'Omaha Burke High School':'OBur','Omaha Burke':'OBur','Burke High School':'OBur','Burke':'OBur',
#                     'Omaha Benson':'OBen','Omaha Benson High School':'OBen',
#                     #Omaha Catholic Schools
#                     'Omaha Skutt Catholic':'Skutt',
#                     'Duchesne':'Duch','Omaha Duchesne Academy':'Duch',
#                     'Creighton Prep':'Prep','Creighton Prep':'Prep',
#                     'Marian':'Marian',
#                     'Brownell-Talbot':'BT', 'Omaha Brownell-Talbot':'BT',

#                     #Yet to be categorized
#                     'Norfolk Senior H.S.':'Norf',
#                     'Norris High School':'Norr', 'Norris':'Norr',
#                     'Douglas County West':'DCW', 'DC West':'DCW',
#                     'Raymond Central':'RC',
#                     'Fremont High School':'Fre',
#                     'Grand Island':'GI','Grand Island Speech':'GI',
#                     'Bennington':'Benn',
#                     'Hastings':'Hast','Hastings Senior High':'Hast',
#                     'Kearney':'Kear',
#                     'North Platte':'NorP',
#                     'Lexington':'Lex',
#                     'Crete High School':'Crete', 'Crete':'Crete',
#                     'Wisner-Pilger':'WisP',
#                     'Siouxland Christian School':'*SxC',
#                     'Atlantic High School':'*Atl',
#                     }
#     return Replacements

# def Standardize_Events():
#     EventDict = {"DI":"DI","HI":"HI","DUO":"DUO","OID":"OID","POE":"POE","POI":"POI","OO":"OO","INF":"INF","ENT":"ENT","EXT":"EXT","IMP":"IMP","Duet":"Duet",
#                  'Dramatic Interpretation':'DI','Oral Interpretation of Serious Prose':'DI','Dramatic Interp':'DI',
#                  'Humorous Interpretation':'HI','Oral Interpretation of Humorous Prose':'HI','Humorous Interp':'HI',
#                  'Poetry':'POE', 'Oral Interpretation of Poetry':'POE','Poetry Interpretation':'POE',
#                  'Program Oral Interp':'POI','Program of Oral Interp.':'POI','Program Oral Interpretation':"POI",'Program of Oral Interpretation':'POI','Program of Interpretation':'POI',
#                  'Duo Interpretation':'DUO','Duo':'DUO','Duet Acting':'DUO',"Duo/Duet Interpretation":"DUO",'Duo Interp':'DUO','Duet Acting/Duo Interp':'DUO',
#                  'Oral Interpretation of Drama':'OID',
#                  'Original Oratory':'OO','Persuasive Speaking':'OO','Persuasive':'OO',
#                  'Informative Speaking':'INF','Informative':'INF',
#                  'Entertainment Speaking':'ENT','Entertainment':'ENT',
#                  'Extemporaneous Speaking':'EXT', 'Extemporaneous':'EXT','Extemp':'EXT',
#                  'Impromptu Speaking':'IMP','Impromptu':'IMP'
#                  }
#     return EventDict

# def Standardize_TournamentOrder(ReturnType):
#     TournamentOrder = {'PLVS':1,
#                        'OBVH':2,
#                        'MS':3,
#                        'Pius X':4,
#                        'LNK':5,
#                        'Norr':6,
#                        'LH':7,
#                        'BW1':8, #TWO TOURNAMENTS
#                        'LSE':9,
#                        'Fre':10,
#                        'EHS':11,
#                        'RC':12,
#                        'LSW':13,
#                        'LNE':14,
#                        'MW':15,
#                        'BW2':16, #TWO TOURNAMENTS
#                        'LNS':17,
#                        'Marian':18,
#                        'MN':19,
#                        'LE':20,
#                        'NQ_N':21,
#                        'NQ_S':22,
#                        'A1':23,
#                        'A2':24,
#                        'A3':25,
#                        'A4':26,
#                        }
#     if ReturnType == 'dict':
#         return TournamentOrder
    
#     elif ReturnType == 'list':
#         TournamentOrder = list(TournamentOrder.keys())
#         return TournamentOrder
    
#     # OLD ORDER :(
#     # if ReturnType == 'dict':
#         # TournamentOrder = {'BW':1,'PLVH':2,'MS':3,'Pius X':4,'Norr':5,'PLVS':6,'LH':7,'Creighton Prep':8,'LSE':9,'Doane':10,'Westside':11,'RC':12,
#                  # 'EHS':13,'LSW':14,'LNE':15,'MW':16,'LNS':17,'Marian':18,'MN':19,'LE':20,'NQ_N':21,'NQ_S':22,'A1':23,'A4':24}
#     # elif ReturnType == 'list':
#         # TournamentOrder = ['BW','PLVH','MS','Pius X','Norr','PLVS','LH','Creighton Prep','LSE',
#                            # 'Doane','Westside','RC','EHS','LSW','LNE','MW','LNS','Marian','MN','LE']

# def Standardize_JudgeNames():
#     JudgeCorrections = {'Emily Glinsman':'Emily Glinsmann',
#                         'Taylor Peterson':'Taylor Petersen',
#                         'Ethan Carslon':'Ethan Carlson',
#                         'George Grinell':'George Grinnell',
#                         'Rachel Vanengen':'Rachel VanEngen',
#                         'Ben Morgan':'Benjamin Morgan',
#                         'Ben Leathers-Arnold':'Benjamin Leathers-Arnold',
#                         'Maddie Stoerp':'Madeline Stoerp',
#                         'Lilly Frields':'Lillian Frields',
#                         'Chloe Meier':'Chloe Meier-Bates', 'C Meier':'Chloe Meier-Bates', 'C Meier Bates':'Chloe Meier-Bates', 'C Meier-Bates':'Chloe Meier-Bates',
#                         'Char Olberding':'Charlotte Olberding',
#                         'Esman Rodas':'Esman Rodas Calderon',
#                         'Travis Grafe':'Travis Grafe-Cline',
#                         'Shreeya Shapokota':'Shreeya Shapkota'}
#     return JudgeCorrections

# def Standardize_MillardNorthNames():
#     Name_Corrections = {'Sophia Naber':'Corey Naber',
#                         'Kennedy Mcknight':'Kennedy McKnight',
#                         # 'Etta Mae Murphy':'Grey Murphy',
#                         # 'Kaiden Carmichael':'Kady Carmichael',
#                         'Gabrielle Burns':'Gabby Burns',
#                         # 'Reagan M. Eigsti':'Reagan Eigsti',
#                         'Cecelia Vlieger':'Cece Vlieger',
#                         # 'Patricia Dunn':'Patsy Dunn',
#                         # 'Zoeann Welch-Ribeiro':'ZoeAnn Welch-Ribeiro',
#                         # 'Caeden Vetro, Etta Mae Murphy':'Caeden Vetro & Grey Murphy',
#                        # 'Harmony Banwo, Patricia Dunn':'Harmony Banwo & Patsy Dunn',
#                        # 'Arpun Kunnath, Tejal Parajuli':'Arpun Kunnath & Tejal Parajuli',
#                        # 'Mary Keeton, Reagan M. Eigsti':'Reagan Eigsti & Mary Keeton'}
#     return Name_Corrections

# def Standardize_CompetitorNames():
#     Name_Corrections = {'Chloe Fiscaro':'Chloe Fisicaro',
#         'Sophie Bathel':'Sophia Bathel',
#         'Anita Mashayekhia':'Anita Mashayekhi',
#         'Vinnie Plasek':'Vixen Plasek','Vinnie Plasek, Zachary Wellman':'Vixen Plasek, Zachary Wellman',
#         'Ben Pelzer':'Benjamin Pelzer','Benjamin R. Pelzer':'Benjamin Pelzer','Benjamin R. Pelzer, Zach Brown':'Benjamin Pelzer, Zach Brown',
#         'Adrien Antunez':'Adrian Antunez',
#         'Jake Sopscich':'Jake Sopsich',
#         'Lilly Leathers':'Lily Leathers',
#         'Sophia Naber':'Corey Naber',
#         }
#     return Name_Corrections

# def Standardize_OIDs():
#     OIDDict = {
#     #Skutt
#     "Grace Bathel, Isaac Jonaitis, Jack Dahms, Noah Stremick, Sophia Bathel":"Grace Bathel, Isaac Jonaitis, Jack Dahms, Noah Stremick, Sophia Bathel","Grace Bathel, Isaac Jonaitis, Jack Dahms, Noah Stremick, Sophie Bathel":"Grace Bathel, Isaac Jonaitis, Jack Dahms, Noah Stremick, Sophia Bathel",
#     #Bennington
#     "Deborah N'Da, Henry Houska, Jack Holtorf, Justine Huse, Nat Rivera":"Deborah N'Da, Justine Huse, Nat Rivera, Jack Holtorf/Ryan Taylor/Henry Houska","Deborah N'Da, Henry Houska, Justine Huse, Nat Rivera, Ryan Taylor":"Deborah N'Da, Justine Huse, Nat Rivera, Jack Holtorf/Ryan Taylor/Henry Houska","Deborah N'Da, Jack Holtorf, Justine Huse, Nat Rivera, Ryan Taylor":"Deborah N'Da, Justine Huse, Nat Rivera, Jack Holtorf/Ryan Taylor/Henry Houska",
#     #Norfolk
#     "Anthony Eppolito, Courtney Matthies, Elliette Mendivil Rodriguez, Ethan Pysher, Kai Vuchetich":"Anthony Eppolito, Courtney Matthies, Ethan Pysher, Kai Vuchetich, Elliette Mendivil Rodriguez/Sherlyn Medina","Anthony Eppolito, Courtney Matthies, Ethan Pysher, Kai Vuchetich, Sherlyn Medina":"Anthony Eppolito, Courtney Matthies, Ethan Pysher, Kai Vuchetich, Elliette Mendivil Rodriguez/Sherlyn Medina",
#     #York
#     "Jack Chavanu , Maelynn Ericson, Nell Chavanu, Raima Kreifels, Taylor Peters":"Jack Chavanu, Maelynn Ericson, Nell Chavanu, Raima Kreifels, Taylor Peters",
#     #Raymond Central
#     "Alliana Miller, Gavin Enevoldsen, Grace Reed, Malayna Mcfarling, Mark Konovalchuck":"Alliana Miller, Gavin Enevoldsen, Grace Reed/Malayna McFarling/Mark Konovalchuck/Josh Greve/Korynn Ball/Ryon Hill","Alliana Miller, Gavin Enevoldsen, Josh Greve, Korynn Ball, Ryon Hill":"Alliana Miller, Gavin Enevoldsen, Grace Reed/Malayna McFarling/Mark Konovalchuck/Josh Greve/Korynn Ball/Ryon Hill",            
#     #Elkhorn
#     "Cadence (Nix) Erwin, Darla Crews, Ellie Cain, Mckenzie Carlson, Yuridia Hernandez-Tapia":"Cadence (Nix) Erwin, Darla Crews, Mckenzie Carlson, Yuridia Hernandez-Tapia, Ellie Cain/Lily Jaworski","Cadence (Nix) Erwin, Darla Crews, Lily Jaworski, Mckenzie Carlson, Yuridia Hernandez-Tapia":"Cadence (Nix) Erwin, Darla Crews, Mckenzie Carlson, Yuridia Hernandez-Tapia, Ellie Cain/Lily Jaworski",
#     #LSW
#     "Audrey Haugen, Brooklyn Bruggeman, Lillian Bittle, Rhea Poda":"Audrey Haugen, Lillian Bittle, Rhea Poda, Brooklyn Bruggeman/Jordyn Davis","Audrey Haugen, Jordyn Davis, Lillian Bittle, Rhea Poda":"Audrey Haugen, Lillian Bittle, Rhea Poda, Brooklyn Bruggeman/Jordyn Davis",
#     #LSE 1    
#     "Aj Lempke, Aolani Wilson, Chantelle Runyan, Phoenix Braatz":"Phoenix Braatz, Chantelle Runyan/Julia Johnson, Aj Lempke/Olivia Nelson, Diwata Patrick/Mia Jensen/Aolani Wilson","Aj Lempke, Chantelle Runyan, Diwata Patrick, Phoenix Braatz":"Phoenix Braatz, Chantelle Runyan/Julia Johnson, Aj Lempke/Olivia Nelson, Diwata Patrick/Mia Jensen/Aolani Wilson","Aj Lempke, Chantelle Runyan, Mia Jensen, Phoenix Braatz":"Phoenix Braatz, Chantelle Runyan/Julia Johnson, Aj Lempke/Olivia Nelson, Diwata Patrick/Mia Jensen/Aolani Wilson","Aj Lempke, Julia Johnson, Mia Jensen, Phoenix Braatz":"Phoenix Braatz, Chantelle Runyan/Julia Johnson, Aj Lempke/Olivia Nelson, Diwata Patrick/Mia Jensen/Aolani Wilson","Chantelle Runyan, Diwata Patrick, Olivia Nelson, Phoenix Braatz":"Phoenix Braatz, Chantelle Runyan/Julia Johnson, Aj Lempke/Olivia Nelson, Diwata Patrick/Mia Jensen/Aolani Wilson",
#     #LSE 2
#     "Avery Bridgford, Bella Mccown, Emi Taylor, Kalainey Nickel, Mia Jensen":"Avery Bridgford, Bella McCown, Emi Taylor, Kalainey Nickel, Mia Jensen/Sydney Kjeldgaard","Avery Bridgford, Bella Mccown, Emi Taylor, Kalainey Nickel, Sydney Kjeldgaard":"Avery Bridgford, Bella McCown, Emi Taylor, Kalainey Nickel, Mia Jensen/Sydney Kjeldgaard",    
#     #LSE 3
#     "Adam Loos, Annise Fatemi, Maddie Skalka, Madeline Jensen, Miriam Peters":"Annise Fatemi, Maddie Skalka, Madeline Jensen, Miriam Peters/Phoenix Krall, Adam Loos/Trent Townsend","Annise Fatemi, Maddie Skalka, Madeline Jensen, Phoenix Krall, Trent Townsend":"Annise Fatemi, Maddie Skalka, Madeline Jensen, Miriam Peters/Phoenix Krall, Adam Loos/Trent Townsend",
#     #Norris 1
#     "Aiyanna Casillas, Brooklyn Ivy, Cass Fejfar, Hays Gorham":"Aiyanna Casillas, Cass Fejfar, Hays Gorham, Brooklyn Ivy/Sydnee Patras","Aiyanna Casillas, Cass Fejfar, Hays Gorham, Sydnee Patras":"Aiyanna Casillas, Cass Fejfar, Hays Gorham, Brooklyn Ivy/Sydnee Patras",
#     #Norris 2
#     "Emilia Frey, Haven Unger, Katelynn Schneider, Matte'A Weber":"Emilia Frey, Katelynn Schneider, Matte'a Weber, Haven Unger/Izzy Lewis","Emilia Frey, Izzy Lewis, Katelynn Schneider, Matte'A Weber":"Emilia Frey, Katelynn Schneider, Matte'a Weber, Haven Unger/Izzy Lewis",
#     #LNS
#     "Kegan Brhel, Maab Amon, Mabruka Mumade, Reyce Usher, Styx Stuart":"Kegan Brhel, Mabruka Mumade, Reyce Usher, Styx Stuart, Maab Amon/Rylee Lieske","Kegan Brhel, Mabruka Mumade, Reyce Usher, Rylee Lieske, Styx Stuart":"Kegan Brhel, Mabruka Mumade, Reyce Usher, Styx Stuart, Maab Amon/Rylee Lieske",
#     #Creighton Prep
#     "Anthony Wellwood, Chris Tollo, Ed Watson, Jack Plambeck":"Chris Tollo, Anthony Wellwood/Will Tabor, Ed Watson/Ethan Schroeder, Joseph Marar/Jack Plambeck/Liam Richardson","Anthony Wellwood, Chris Tollo, Ed Watson, Joseph Marar":"Chris Tollo, Anthony Wellwood/Will Tabor, Ed Watson/Ethan Schroeder, Joseph Marar/Jack Plambeck/Liam Richardson","Anthony Wellwood, Chris Tollo, Ed Watson, Liam Richardson":"Chris Tollo, Anthony Wellwood/Will Tabor, Ed Watson/Ethan Schroeder, Joseph Marar/Jack Plambeck/Liam Richardson","Anthony Wellwood, Chris Tollo, Ethan Schroeder, Joseph Marar":"Chris Tollo, Anthony Wellwood/Will Tabor, Ed Watson/Ethan Schroeder, Joseph Marar/Jack Plambeck/Liam Richardson","Chris Tollo, Ed Watson, Joseph Marar, Will Tabor":"Chris Tollo, Anthony Wellwood/Will Tabor, Ed Watson/Ethan Schroeder, Joseph Marar/Jack Plambeck/Liam Richardson",
#     #Nebraska City
#     "Blayne Rumery, Dallas Mueller-Pry, Madi Tietz, Mason Ottemann, Timmy Stanek":"Dallas Mueller-Pry, Madisen Tietz, Mason Ottemann, Timothy Stanek, Blayne/Theodore Rumery","Dallas Mueller-Pry, Madisen Tietz, Mason Ottemann, Theodore Rumery, Timothy Stanek":"Dallas Mueller-Pry, Madisen Tietz, Mason Ottemann, Timothy Stanek, Blayne/Theodore Rumery",
#     #Plattsmouth 1
#     "Gabe Spicer, Gillyan Wilson, Lucy Alldredge, Madeleine Harvey, Megan Graves":"Gabe Spicer, Gillyan Wilson, Lucy Alldredge, Madeleine Harvey, Megan Graves/Sophia Alldredge","Gabe Spicer, Gillyan Wilson, Lucy Alldredge, Madeleine Harvey, Sophia Alldredge":"Gabe Spicer, Gillyan Wilson, Lucy Alldredge, Madeleine Harvey, Megan Graves/Sophia Alldredge",
#     #Plattsmouth 2
#     "Dodani Cruz-Rivera, Jaxon Sharp, Lilyanna Guthner, Michael Guthner":"Jaxon Sharp, Lilyanna Guthner, Michael Guthner, Dodani Cruz-Rivera/Isabelle McGraw","Isabelle Mcgraw, Jaxon Sharp, Lilyanna Guthner, Michael Guthner":"Jaxon Sharp, Lilyanna Guthner, Michael Guthner, Dodani Cruz-Rivera/Isabelle McGraw",
#     #Scottsbluff 1        
#     "Brandon Baker, Ella Anderson, Jayden Lindley, Lauren Johnson, Nathaniel Wilson":"Brandon Baker, Ella Anderson, Nathaniel Wilson, Lauren Johnson/Marley Wineman, Jayden Lindley/Susan Anderson","Brandon Baker, Ella Anderson, Lauren Johnson, Nathaniel Wilson, Susan Anderson":"Brandon Baker, Ella Anderson, Nathaniel Wilson, Lauren Johnson/Marley Wineman, Jayden Lindley/Susan Anderson","Brandon Baker, Ella Anderson, Marley Wineman, Nathaniel Wilson, Susan Anderson":"Brandon Baker, Ella Anderson, Nathaniel Wilson, Lauren Johnson/Marley Wineman, Jayden Lindley/Susan Anderson",
#     #Scottsbluff 2
#     "Drew Kaufman, Hilario Vaquera, Lauren Johnson, Marlowe Osborn, Tucker Baker":"Drew Kaufman, Hilario Vaquera, Marlowe Osborn, Tucker Baker, Lauren Johnson/Susan Anderson/Ava Osborn","Drew Kaufman, Hilario Vaquera, Marlowe Osborn, Susan Anderson, Tucker Baker":"Drew Kaufman, Hilario Vaquera, Marlowe Osborn, Tucker Baker, Lauren Johnson/Susan Anderson/Ava Osborn","Ava Osborn, Drew Kaufman, Hilario Vaquera, Marlowe Osborn, Tucker Baker":"Drew Kaufman, Hilario Vaquera, Marlowe Osborn, Tucker Baker, Lauren Johnson/Susan Anderson/Ava Osborn"   
#     }
#     #92 OIDs down to:
#     return OIDDict