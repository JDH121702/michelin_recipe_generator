# Chef profiles for the Michelin Star Recipe Generator
# Contains information about renowned Michelin-starred chefs, their cooking styles,
# signature techniques, and specialty cuisines

CHEF_PROFILES = {
    "thomas_keller": {
        "name": "Thomas Keller",
        "restaurants": ["The French Laundry", "Per Se"],
        "style": "French-American, precision cooking",
        "signature": "Refined simplicity, perfect execution",
        "techniques": ["Classical French techniques", "Modern precision", "Sous vide mastery"],
        "specialty_cuisines": ["French", "American"],
        "famous_dishes": ["Oysters and Pearls", "Salmon Cornets", "Coffee and Doughnuts"],
        "bio": "Thomas Keller is a renowned American chef known for his culinary skills and his award-winning restaurants. He is the only American chef to have been awarded simultaneous three-star Michelin ratings for two different restaurants.",
        "image": "thomas_keller.jpg"
    },
    
    "niki_nakayama": {
        "name": "Niki Nakayama",
        "restaurants": ["n/naka"],
        "style": "Modern kaiseki, Japanese",
        "signature": "Seasonal progression, artistic presentation",
        "techniques": ["Traditional Japanese", "Contemporary influences", "Kaiseki principles"],
        "specialty_cuisines": ["Japanese", "Kaiseki"],
        "famous_dishes": ["Shiizakana", "Modern Zukuri", "Hassun"],
        "bio": "Niki Nakayama is a Japanese-American chef and owner of n/naka in Los Angeles, specializing in modern Japanese kaiseki cuisine. Her restaurant has received two Michelin stars and was featured on Netflix's Chef's Table.",
        "image": "niki_nakayama.jpg"
    },
    
    "gordon_ramsay": {
        "name": "Gordon Ramsay",
        "restaurants": ["Restaurant Gordon Ramsay", "Petrus", "Gordon Ramsay au Trianon"],
        "style": "Modern French, British",
        "signature": "Bold flavors, technical perfection",
        "techniques": ["Classical French foundation", "Contemporary flair", "Precise execution"],
        "specialty_cuisines": ["French", "British"],
        "famous_dishes": ["Beef Wellington", "Scrambled Eggs", "Lobster Ravioli"],
        "bio": "Gordon Ramsay is a British chef, restaurateur, and television personality. His restaurants have been awarded 16 Michelin stars in total, and he is known for his fiery temperament and exceptional culinary skills.",
        "image": "gordon_ramsay.jpg"
    },
    
    "dominique_crenn": {
        "name": "Dominique Crenn",
        "restaurants": ["Atelier Crenn", "Bar Crenn"],
        "style": "Artistic French, poetic cuisine",
        "signature": "Storytelling through food, artistic presentation",
        "techniques": ["Modern techniques", "Artistic expression", "Sustainable practices"],
        "specialty_cuisines": ["French", "Artistic"],
        "famous_dishes": ["A Walk in the Forest", "Geoduck Tart", "Brioche Feuilletée"],
        "bio": "Dominique Crenn is a French chef and the first female chef in the United States to receive three Michelin stars, for her restaurant Atelier Crenn. Her cuisine is known for its poetic and artistic qualities.",
        "image": "dominique_crenn.jpg"
    },
    
    "massimo_bottura": {
        "name": "Massimo Bottura",
        "restaurants": ["Osteria Francescana", "Franceschetta 58"],
        "style": "Modern Italian, avant-garde",
        "signature": "Reinterpreting Italian classics, playful presentation",
        "techniques": ["Traditional Italian", "Contemporary innovation", "Conceptual cuisine"],
        "specialty_cuisines": ["Italian", "Avant-garde"],
        "famous_dishes": ["Five Ages of Parmigiano Reggiano", "Oops! I Dropped the Lemon Tart", "The Crunchy Part of the Lasagna"],
        "bio": "Massimo Bottura is an Italian chef and restaurateur. His restaurant, Osteria Francescana, has been rated as one of the best restaurants in the world and has received three Michelin stars. He is known for his innovative takes on traditional Italian cuisine.",
        "image": "massimo_bottura.jpg"
    },
    
    "rene_redzepi": {
        "name": "René Redzepi",
        "restaurants": ["Noma"],
        "style": "New Nordic, foraging-based",
        "signature": "Hyperlocal ingredients, fermentation",
        "techniques": ["Foraging", "Fermentation", "Preservation"],
        "specialty_cuisines": ["Nordic", "Seasonal"],
        "famous_dishes": ["Vintage Carrot and Chamomile", "Sea Urchin and Hazelnuts", "Beef Tartar and Ants"],
        "bio": "René Redzepi is a Danish chef and co-owner of the two-Michelin star restaurant Noma in Copenhagen, Denmark. Noma has been ranked as the Best Restaurant in the World multiple times, and Redzepi is known for his focus on foraging and the New Nordic Cuisine movement.",
        "image": "rene_redzepi.jpg"
    },
    
    "grant_achatz": {
        "name": "Grant Achatz",
        "restaurants": ["Alinea", "Next", "The Aviary"],
        "style": "Molecular gastronomy, progressive American",
        "signature": "Theatrical presentation, innovative techniques",
        "techniques": ["Molecular gastronomy", "Avant-garde", "Sensory manipulation"],
        "specialty_cuisines": ["Progressive American", "Molecular"],
        "famous_dishes": ["Black Truffle Explosion", "Edible Balloon", "Tabletop Dessert"],
        "bio": "Grant Achatz is an American chef and restaurateur known for his contributions to molecular gastronomy and progressive cuisine. His Chicago restaurant Alinea has been awarded three Michelin stars and is known for its innovative and theatrical approach to dining.",
        "image": "grant_achatz.jpg"
    },
    
    "clare_smyth": {
        "name": "Clare Smyth",
        "restaurants": ["Core by Clare Smyth"],
        "style": "Modern British, sustainable luxury",
        "signature": "Elevated British ingredients, elegant simplicity",
        "techniques": ["Classic techniques", "Modern interpretation", "Sustainable focus"],
        "specialty_cuisines": ["British", "Sustainable"],
        "famous_dishes": ["Potato and Roe", "Lamb Carrot", "Core Apple"],
        "bio": "Clare Smyth is a British chef and the first and only female chef to run a restaurant with three Michelin stars in the UK. Her restaurant Core by Clare Smyth has received three Michelin stars and is known for its focus on sustainable British cuisine.",
        "image": "clare_smyth.jpg"
    }
}

# Chef influence descriptions - used to explain how each chef's style affects recipes
CHEF_INFLUENCE_DESCRIPTIONS = {
    "thomas_keller": {
        "high": "Precise French techniques with immaculate presentation and refined flavors. Emphasis on perfect execution and the highest quality ingredients.",
        "medium": "Clean flavors with French influence and attention to technical detail. Balance of simplicity and sophistication.",
        "low": "Subtle influence of French techniques with an emphasis on ingredient quality."
    },
    
    "niki_nakayama": {
        "high": "Seasonal Japanese kaiseki progression with artistic presentation. Emphasis on texture contrasts and subtle, pure flavors.",
        "medium": "Japanese influences with seasonal ingredients and balanced flavor profiles. Attention to visual composition.",
        "low": "Subtle Japanese elements with seasonal awareness and clean presentation."
    },
    
    "gordon_ramsay": {
        "high": "Bold, intense flavors with technical precision. Classic French foundation with modern British influences.",
        "medium": "Well-defined flavors with technical accuracy. Balance of classic and contemporary techniques.",
        "low": "Straightforward preparation with emphasis on bringing out natural flavors."
    },
    
    "dominique_crenn": {
        "high": "Poetic, artistic presentation with French techniques. Emphasis on storytelling through food and visual impact.",
        "medium": "Creative presentation with French influences. Balance of artistic elements and flavor focus.",
        "low": "Subtle artistic touches with clean flavors and elegant presentation."
    },
    
    "massimo_bottura": {
        "high": "Playful reinterpretation of Italian classics with conceptual elements. Bold flavors with surprising presentations.",
        "medium": "Italian influences with creative twists. Traditional flavors presented in modern ways.",
        "low": "Subtle Italian elements with occasional unexpected combinations."
    },
    
    "rene_redzepi": {
        "high": "Hyperlocal, foraged ingredients with fermentation techniques. Emphasis on natural preservation methods and pure flavors.",
        "medium": "Seasonal focus with some foraged elements. Balanced use of preservation techniques.",
        "low": "Subtle use of seasonal ingredients with minimal processing."
    },
    
    "grant_achatz": {
        "high": "Theatrical, avant-garde presentation with molecular techniques. Multi-sensory experience with unexpected textures.",
        "medium": "Creative presentation with some molecular elements. Balance of innovation and flavor focus.",
        "low": "Subtle creative touches with occasional unexpected textures or presentations."
    },
    
    "clare_smyth": {
        "high": "Elevated British ingredients with sustainable luxury. Elegant simplicity with perfect technical execution.",
        "medium": "Quality ingredients with sustainable focus. Clean presentation with technical precision.",
        "low": "Subtle emphasis on ingredient quality with minimal manipulation."
    }
}