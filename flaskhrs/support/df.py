driven_factors = {
    "smk": [
        (0, 'Never'),
        (1, 'Active'),
        (2, 'Ex-active'),
    ]
    ,
    "boolChoice": [
        ('1', 'Yes'),
        ('0', 'No'),
    ],
    "MaritalStatus": [
        (0, 'Never Married'),
        (1, 'Widowed Young <40'),
        (2, 'Widowed Old >40'),
        (3, 'Divorced Male'),
        (4, 'Divorced Female'),
        (5, 'Married'),
    ],
    "Race": [
        (0, 'White'),
        (1, 'Black'),
        (2, 'American Indian'),
        (3, 'Asian'),
        (4, 'Hispanic'),
    ],

    "Education": [
        (0, 'Less than high school'),
        (1, 'High school'),
        (2, 'More than high school'),
    ],

    "BMI": [
        (0, 'Underweight'),
        (1, 'Normal'),
        (2, 'Overweight'),
        (3, 'Obesity I'),
        (4, 'Obesity II'),
        (5, 'Extreme Obesity')
    ],

    "Alcohol": [
        (0, 'Never'),
        (1, 'Rarely'),
        (2, '2-3 Drinks a Week'),
        (3, '3-7 Drinks a Week'),
        (4, '8+ Drinks a Week'),
    ],

    "Physical Activity": [
        (0, 'Never'),
        (1, 'Rarely'),
        (2, '2-3 Days a Week'),
        (3, '3-7 Days a Week'),
        (4, '8+ Days a Week'),
    ],

    "A1c": lambda a1c: 1.16 ** (a1c - 6.5),
}

hr = {
    "marital": (1.1, 1, 1.2, 1, 1, 0.8,),
    "race": (1.0, 1.1, 1.2, 1.3, 1.4,),
    "education": (1.0, 1.1, 1.2, 1.3, 1.4,),
    "alcohol": (1.0, 1.1, 1.2, 1.3, 1.4,),
    "physical": (1.0, 1.1, 1.2, 1.3, 1.4,),
}


def get_choices(key):
    return driven_factors.get(key)


def get_hr(key):
    return hr.get(key)
