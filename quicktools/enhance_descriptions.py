import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# Enhance descriptions
# Just a broad replace for common short descriptions
replacements = [
    ("'Daily water need (L).'", "'Calculate your recommended daily water intake in liters.'"),
    ("'Est. Body Fat %.'", "'Estimate your body fat percentage using the US Navy method.'"),
    ("'Basal Metabolic Rate.'", "'Calculate your Basal Metabolic Rate (BMR) calories.'"),
    ("'Monthly payment.'", "'Estimate your monthly mortgage payments.'"),
    ("'Simple XML Indent.'", "'Format and indent your XML code automatically.'"),
    ("'Indent XML.'", "'Format and indent your XML code automatically.'"),
    ("'Generate QR Code.'", "'Create a QR Code for any text or URL instantly.'"),
    ("'Nth number.'", "'Calculate the Nth number in the Fibonacci sequence.'"),
    ("'Sqrt(x)'", "'Calculate the square root of a number.'"),
    ("'Cbrt(x)'", "'Calculate the cube root of a number.'"),
    ("'Log10(x)'", "'Calculate the base-10 logarithm of a number.'"),
    ("'Ln(x)'", "'Calculate the natural logarithm of a number.'"),
    ("'Sin(x deg)'", "'Calculate the sine of an angle in degrees.'"),
    ("'Cos(x deg)'", "'Calculate the cosine of an angle in degrees.'"),
    ("'Tan(x deg)'", "'Calculate the tangent of an angle in degrees.'"),
    ("'Average of list.'", "'Calculate the mean (average) of a list of numbers.'"),
    ("'Median of list.'", "'Calculate the median value of a list of numbers.'"),
    ("'Repeat text N times (use line1 for N).'", "'Repeat a string N times (specify N on the first line).'"),
    ("'Pad text start.'", "'Pad the start of each line with spaces.'"),
    ("'Octal to Symbol (e.g. 755).'", "'Convert chmod octal permissions to symbolic notation.'"),
    ("'Lookup Code.'", "'Lookup the meaning of HTTP status codes.'"),
    ("'Ideal Weight (kg).'", "'Calculate your ideal body weight using the Devine formula.'"),
    ("'Years to double inv.'", "'Estimate years to double your investment using Rule of 72.'"),
    ("'Pressure.'", "'Convert pressure units (Bar, PSI, etc.).'"),
    ("'Force.'", "'Convert force units (Newtons, Pounds-force, etc.).'"),
    ("'Random boolean.'", "'Generate a random True or False value.'"),
    ("'Past 50 years.'", "'Generate a random date within the past 50 years.'"),
    ("'Time.'", "'Convert various time units.'"),
    ("'Data.'", "'Convert digital data storage units.'"),
    ("'Mass.'", "'Convert mass and weight units.'"),
    ("'Volume.'", "'Convert volume units.'"),
    ("'Area.'", "'Convert area units.'"),
    ("'Length.'", "'Convert length and distance units.'"),
    ("'Simple Avg.'", "'Calculate a simple average GPA.'"),
    ("'Minify HTML.'", "'Minify your HTML code by removing whitespace.'"),
    ("'Create tags.'", "'Generate hashtags from a text string.'"),
    ("'Binary to Hex.'", "'Convert binary strings to hexadecimal format.'"),
    ("'Hex to Binary.'", "'Convert hexadecimal strings to binary format.'"),
    ("'Download Speed Test.'", "'Test your internet download speed (approximate).'"),
    ("'Return on Investment.'", "'Calculate the percentage return on an investment.'"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('quicktools/index.html', 'w') as f:
    f.write(content)
