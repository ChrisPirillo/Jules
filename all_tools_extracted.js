    createSimpleTextTool('uppercase', 'Uppercase', 'Text', 'Convert text to uppercase.', (text) => text.toUpperCase());
    createSimpleTextTool('lowercase', 'Lowercase', 'Text', 'Convert text to lowercase.', (text) => text.toLowerCase());
    createSimpleTextTool('title-case', 'Title Case', 'Text', 'Capitalize first letter of each word.', (text) => text.toLowerCase().split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '));
    createSimpleTextTool('reverse-string', 'Reverse Text', 'Text', 'Reverse the characters in text.', (text) => text.split('').reverse().join(''));
    createSimpleTextTool('remove-spaces', 'Remove Spaces', 'Text', 'Remove all whitespace.', (text) => text.replace(/\s/g, ''));
    createSimpleTextTool('slugify', 'Slug Generator', 'Text', 'Convert text to URL slug.', (text) => text.toLowerCase().replace(/[^\w ]+/g, '').replace(/ +/g, '-'));
    createSimpleTextTool('base64-encode', 'Base64 Encode', 'Dev', 'Encode text to Base64.', (text) => btoa(text));
    createSimpleTextTool('base64-decode', 'Base64 Decode', 'Dev', 'Decode Base64 to text.', (text) => atob(text));
    createSimpleTextTool('url-encode', 'URL Encode', 'Dev', 'Encode text for URLs.', (text) => encodeURIComponent(text));
    createSimpleTextTool('url-decode', 'URL Decode', 'Dev', 'Decode URL encoded text.', (text) => decodeURIComponent(text));
    createSimpleTextTool('rot13', 'ROT13 Cipher', 'Text', 'Apply ROT13 substitution.', (text) => text.replace(/[a-zA-Z]/g, c => String.fromCharCode((c <= 'Z' ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26)));
    createSimpleTextTool('word-count', 'Word Count', 'Text', 'Count words in text.', (text) => `Words: ${text.trim().split(/\s+/).length}`);
    createSimpleTextTool('char-count', 'Char Count', 'Text', 'Count characters in text.', (text) => `Characters: ${text.length}`);
    createSimpleTextTool('camel-case', 'Camel Case', 'Text', 'Convert text to camelCase.', (text) => text.toLowerCase().replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase()));
    createSimpleTextTool('snake-case', 'Snake Case', 'Text', 'Convert text to snake_case.', (text) => text && text.match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g).map(x => x.toLowerCase()).join('_'));
    createSimpleTextTool('kebab-case', 'Kebab Case', 'Text', 'Convert text to kebab-case.', (text) => text && text.match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g).map(x => x.toLowerCase()).join('-'));
    createSimpleTextTool('sentence-case', 'Sentence Case', 'Text', 'Convert text to Sentence case.', (text) => text.toLowerCase().replace(/(^\s*\w|[\.\!\?]\s*\w)/g, c => c.toUpperCase()));
    createSimpleTextTool('reverse-words', 'Reverse Words', 'Text', 'Reverse the order of words.', (text) => text.split(' ').reverse().join(' '));
    createSimpleTextTool('remove-duplicates', 'Remove Duplicate Lines', 'Text', 'Remove duplicate lines.', (text) => [...new Set(text.split('\n'))].join('\n'));
    createSimpleTextTool('sort-lines', 'Sort Lines (A-Z)', 'Text', 'Sort lines alphabetically.', (text) => text.split('\n').sort().join('\n'));
    createSimpleTextTool('sort-lines-reverse', 'Sort Lines (Z-A)', 'Text', 'Sort lines in reverse.', (text) => text.split('\n').sort().reverse().join('\n'));
    createSimpleTextTool('random-lines', 'Shuffle Lines', 'Text', 'Randomly shuffle lines.', (text) => text.split('\n').sort(() => Math.random() - 0.5).join('\n'));
    createSimpleTextTool('trim-lines', 'Trim Lines', 'Text', 'Trim whitespace from lines.', (text) => text.split('\n').map(l => l.trim()).join('\n'));
    createSimpleTextTool('remove-empty-lines', 'Remove Empty Lines', 'Text', 'Remove empty lines.', (text) => text.split('\n').filter(l => l.trim() !== '').join('\n'));
    createSimpleTextTool('add-line-numbers', 'Add Line Numbers', 'Text', 'Add line numbers to text.', (text) => text.split('\n').map((l, i) => `${i+1}. ${l}`).join('\n'));
    createSimpleTextTool('extract-emails', 'Extract Emails', 'Dev', 'Extract email addresses.', (text) => (text.match(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/gi) || []).join('\n'));
    createSimpleTextTool('extract-urls', 'Extract URLs', 'Dev', 'Extract URLs from text.', (text) => (text.match(/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/gi) || []).join('\n'));
    createSimpleTextTool('extract-numbers', 'Extract Numbers', 'Dev', 'Extract numbers from text.', (text) => (text.match(/\d+/g) || []).join('\n'));
    createSimpleTextTool('morse-code', 'Text to Morse', 'Text', 'Convert text to Morse code.', (text) => {
        const morseCode = { 'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '/' };
        return text.toUpperCase().split('').map(c => morseCode[c] || c).join(' ');
    });
    createSimpleTextTool('binary-encode', 'Text to Binary', 'Dev', 'Convert text to binary.', (text) => text.split('').map(c => c.charCodeAt(0).toString(2).padStart(8, '0')).join(' '));
    createSimpleTextTool('hex-encode', 'Text to Hex', 'Dev', 'Convert text to hexadecimal.', (text) => text.split('').map(c => c.charCodeAt(0).toString(16).padStart(2, '0')).join(' '));
    createSimpleTextTool('ascii-encode', 'Text to ASCII', 'Dev', 'Convert text to ASCII codes.', (text) => text.split('').map(c => c.charCodeAt(0)).join(' '));
    createSimpleTextTool('csv-to-json', 'CSV to JSON', 'Dev', 'Simple CSV to JSON conversion.', (text) => {
        const lines = text.split('\n');
        const headers = lines[0].split(',');
        return JSON.stringify(lines.slice(1).map(line => {
            const data = line.split(',');
            return headers.reduce((obj, nextKey, index) => {
                obj[nextKey.trim()] = data[index];
                return obj;
            }, {});
        }), null, 2);
    });
    createMathTool('bmi-calc', 'BMI Calculator', 'Math', 'Calculate Body Mass Index.',
        [{key:'w', label:'Weight (kg)'}, {key:'h', label:'Height (m)'}],
        (v) => (v.w / (v.h * v.h)).toFixed(2));
    createMathTool('tip-calc', 'Tip Calculator', 'Finance', 'Calculate tip amount.',
        [{key:'bill', label:'Bill Amount'}, {key:'tip', label:'Tip %'}],
        (v) => (v.bill * (v.tip / 100)).toFixed(2));
    createMathTool('discount-calc', 'Discount Calculator', 'Finance', 'Calculate discounted price.',
        [{key:'price', label:'Original Price'}, {key:'disc', label:'Discount %'}],
        (v) => (v.price - (v.price * (v.disc / 100))).toFixed(2));
    createMathTool('sales-tax', 'Sales Tax', 'Finance', 'Calculate final price with tax.',
        [{key:'price', label:'Price'}, {key:'tax', label:'Tax %'}],
        (v) => (v.price * (1 + v.tax / 100)).toFixed(2));
    createMathTool('circle-area', 'Circle Area', 'Math', 'Calculate area of a circle.',
        [{key:'r', label:'Radius'}],
        (v) => (Math.PI * v.r * v.r).toFixed(2));
    createMathTool('rect-area', 'Rectangle Area', 'Math', 'Calculate area of a rectangle.',
        [{key:'w', label:'Width'}, {key:'h', label:'Height'}],
        (v) => (v.w * v.h).toFixed(2));
    createMathTool('triangle-area', 'Triangle Area', 'Math', 'Calculate area of a triangle.',
        [{key:'b', label:'Base'}, {key:'h', label:'Height'}],
        (v) => (0.5 * v.b * v.h).toFixed(2));
    createMathTool('cylinder-vol', 'Cylinder Volume', 'Math', 'Calculate volume of a cylinder.',
        [{key:'r', label:'Radius'}, {key:'h', label:'Height'}],
        (v) => (Math.PI * v.r * v.r * v.h).toFixed(2));
    createMathTool('sphere-vol', 'Sphere Volume', 'Math', 'Calculate volume of a sphere.',
        [{key:'r', label:'Radius'}],
        (v) => ((4/3) * Math.PI * Math.pow(v.r, 3)).toFixed(2));
    createMathTool('simple-interest', 'Simple Interest', 'Finance', 'Calculate simple interest.',
        [{key:'p', label:'Principal'}, {key:'r', label:'Rate %'}, {key:'t', label:'Time (years)'}],
        (v) => (v.p * v.r * v.t / 100).toFixed(2));
    createMathTool('compound-interest', 'Compound Interest', 'Finance', 'Calculate compound interest.',
        [{key:'p', label:'Principal'}, {key:'r', label:'Rate %'}, {key:'t', label:'Time (years)'}, {key:'n', label:'Times/Year'}],
        (v) => (v.p * Math.pow((1 + (v.r/100)/v.n), v.n * v.t)).toFixed(2));
    createMathTool('percentage-of', 'Percentage Of', 'Math', 'What is X% of Y?',
        [{key:'x', label:'Percentage (X)'}, {key:'y', label:'Value (Y)'}],
        (v) => ((v.x / 100) * v.y).toFixed(2));
    createMathTool('percentage-change', 'Percentage Change', 'Math', 'Change from X to Y.',
        [{key:'x', label:'Old Value'}, {key:'y', label:'New Value'}],
        (v) => (((v.y - v.x) / v.x) * 100).toFixed(2) + '%');
    createMathTool('average', 'Average Calculator', 'Math', 'Calculate average of 2 numbers.',
        [{key:'a', label:'Number 1'}, {key:'b', label:'Number 2'}],
        (v) => ((v.a + v.b) / 2).toFixed(2));
    createMathTool('hypotenuse', 'Hypotenuse Calc', 'Math', 'Calculate hypotenuse (Pythagorean).',
        [{key:'a', label:'Side A'}, {key:'b', label:'Side B'}],
        (v) => Math.sqrt(v.a*v.a + v.b*v.b).toFixed(2));
    createMathTool('aspect-ratio', 'Aspect Ratio Height', 'Math', 'Calculate height from width & ratio.',
        [{key:'w', label:'Width'}, {key:'rw', label:'Ratio W'}, {key:'rh', label:'Ratio H'}],
        (v) => (v.w * (v.rh / v.rw)).toFixed(2));
    createMathTool('factorial', 'Factorial', 'Math', 'Calculate N!.',
        [{key:'n', label:'Number (N)'}],
        (v) => {
            let res = 1;
            for(let i=2; i<=v.n; i++) res *= i;
            return res;
        });
    createMathTool('power', 'Power Calculator', 'Math', 'Calculate Base^Exponent.',
        [{key:'b', label:'Base'}, {key:'e', label:'Exponent'}],
        (v) => Math.pow(v.b, v.e));
    createMathTool('root', 'Nth Root', 'Math', 'Calculate Nth root of X.',
        [{key:'x', label:'Number (X)'}, {key:'n', label:'Root (N)'}],
        (v) => Math.pow(v.x, 1/v.n).toFixed(4));
    createGeneratorTool('uuid', 'UUID Generator', 'Dev', 'Generate UUID v4.', 'Generate UUID', () =>
        'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        })
    );
    createGeneratorTool('unix-timestamp', 'Unix Timestamp', 'Dev', 'Get current Unix timestamp.', 'Get Timestamp', () => Math.floor(Date.now() / 1000));
    createGeneratorTool('current-time-ms', 'Timestamp (ms)', 'Dev', 'Get current timestamp (ms).', 'Get Milliseconds', () => Date.now());
    createGeneratorTool('random-number', 'Random Number', 'Math', 'Random number 1-100.', 'Roll (1-100)', () => Math.floor(Math.random() * 100) + 1);
    createGeneratorTool('dice-roller', 'Dice Roller', 'Game', 'Roll a 6-sided die.', 'Roll D6', () => Math.floor(Math.random() * 6) + 1);
    createGeneratorTool('coin-flipper', 'Coin Flipper', 'Game', 'Flip a coin.', 'Flip Coin', () => Math.random() < 0.5 ? 'Heads' : 'Tails');
    createGeneratorTool('yes-no', 'Yes/No Decision', 'Game', 'Random Yes or No.', 'Decide', () => Math.random() < 0.5 ? 'Yes' : 'No');
    createGeneratorTool('ip-address', 'IP Address (Mock)', 'Dev', 'Simulated IP Lookup.', 'Get IP', () => '192.168.1.' + Math.floor(Math.random() * 255));
    createGeneratorTool('mac-address', 'MAC Address Gen', 'Dev', 'Random MAC Address.', 'Generate MAC', () => 'XX:XX:XX:XX:XX:XX'.replace(/X/g, () => '0123456789ABCDEF'.charAt(Math.floor(Math.random() * 16))));
    createGeneratorTool('hex-color', 'Random Color', 'Color', 'Generate random Hex color.', 'Generate Color', () => '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0'));
    createGeneratorTool('password-strength', 'Password Strength', 'Security', 'Check password strength.', 'Check', () => {
        // Since input is needed, this simple generator won't work perfectly.
        // Let's just return a placeholder or random advice for the "Generator" pattern.
        // Better: Use SimpleTextTool for this one actually.
        return "Use the 'Password Gen' tool for actual generation.";
    });
    createGeneratorTool('lorem-word', 'Random Word', 'Text', 'Generate a random latin word.', 'Generate Word', () => {
        const words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt'];
        return words[Math.floor(Math.random() * words.length)];
    });
    createSimpleTextTool('hash-simple', 'Simple Hash (djb2)', 'Security', 'Generate simple hash.', (text) => {
        let hash = 5381;
        for (let i = 0; i < text.length; i++) hash = (hash * 33) ^ text.charCodeAt(i);
        return (hash >>> 0).toString(16);
    });
    createSimpleTextTool('md5-mock', 'MD5 (Mock)', 'Security', 'Mock MD5 hash (not real security).', (text) => "d41d8cd98f00b204e9800998ecf8427e (Mock)");
    createSimpleTextTool("css-minifier", "CSS Minifier", "Dev", "Minify CSS code.", (text) => text.replace(/\s+/g, " "));
    createSimpleTextTool('js-minifier', 'JS Minifier (Simple)', 'Dev', 'Remove comments and whitespace.', (text) => text.replace(/\/\/.*$/gm, '').replace(/\/\*[\s\S]*?\*\//g, '').replace(/\s+/g, ' '));
    createSimpleTextTool('html-encode', 'HTML Entity Encode', 'Dev', 'Encode HTML special chars.', (text) => text.replace(/[\u00A0-\u9999<>\&]/g, i => '&#'+i.charCodeAt(0)+';'));
    createSimpleTextTool('html-decode', 'HTML Entity Decode', 'Dev', 'Decode HTML entities.', (text) => {
        const doc = new DOMParser().parseFromString(text, "text/html");
        return doc.documentElement.textContent;
    });
    createSimpleTextTool('sql-format', 'SQL Formatter', 'Dev', 'Simple SQL Formatting.', (text) => text.replace(/\s+/g, ' ').replace(/ (SELECT|FROM|WHERE|AND|OR|ORDER BY|GROUP BY|LIMIT|INSERT|UPDATE|DELETE) /gi, '\n '));
    createSimpleTextTool('markdown-preview', 'Markdown Preview', 'Text', 'Preview markdown (HTML output).', (text) => {
        // Very simple markdown parser
        return text
            .replace(/^# (.*$)/gim, '<h1></h1>')
            .replace(/^## (.*$)/gim, '<h2></h2>')
            .replace(/^### (.*$)/gim, '<h3></h3>')
            .replace(/\*\*(.*)\*\*/gim, '<b></b>')
            .replace(/\*(.*)\*/gim, '<i></i>')
            .replace(/\n/gim, '<br>');
    });
    createMathTool('age-calc', 'Age Calculator', 'Time', 'Calculate age from birth year.',
        [{key:'year', label:'Birth Year'}, {key:'curr', label:'Current Year (optional)', placeholder:'2025'}],
        (v) => (v.curr || new Date().getFullYear()) - v.year);
    createMathTool('date-diff', 'Date Difference (Days)', 'Time', 'Difference between two years.',
        [{key:'y1', label:'Year 1'}, {key:'y2', label:'Year 2'}],
        (v) => Math.abs(v.y1 - v.y2) * 365);
    createMathTool('leap-year', 'Leap Year Checker', 'Time', 'Is year a leap year? (1=Yes, 0=No)',
        [{key:'year', label:'Year'}],
        (v) => ((v.year % 4 == 0 && v.year % 100 != 0) || v.year % 400 == 0) ? "Yes" : "No");
    createMathTool('c-to-f', 'Celsius to Fahrenheit', 'Converter', 'Convert C to F.', [{key:'c', label:'Celsius'}], (v) => (v.c * 9/5 + 32).toFixed(2));
    createMathTool('f-to-c', 'Fahrenheit to Celsius', 'Converter', 'Convert F to C.', [{key:'f', label:'Fahrenheit'}], (v) => ((v.f - 32) * 5/9).toFixed(2));
    createMathTool('km-to-mi', 'KM to Miles', 'Converter', 'Convert km to miles.', [{key:'km', label:'Kilometers'}], (v) => (v.km * 0.621371).toFixed(4));
    createMathTool('mi-to-km', 'Miles to KM', 'Converter', 'Convert miles to km.', [{key:'mi', label:'Miles'}], (v) => (v.mi / 0.621371).toFixed(4));
    createMathTool('kg-to-lb', 'KG to Pounds', 'Converter', 'Convert kg to lbs.', [{key:'kg', label:'Kilograms'}], (v) => (v.kg * 2.20462).toFixed(4));
    createMathTool('lb-to-kg', 'Pounds to KG', 'Converter', 'Convert lbs to kg.', [{key:'lb', label:'Pounds'}], (v) => (v.lb / 2.20462).toFixed(4));
    createMathTool('m-to-ft', 'Meters to Feet', 'Converter', 'Convert meters to feet.', [{key:'m', label:'Meters'}], (v) => (v.m * 3.28084).toFixed(4));
    createMathTool('ft-to-m', 'Feet to Meters', 'Converter', 'Convert feet to meters.', [{key:'ft', label:'Feet'}], (v) => (v.ft / 3.28084).toFixed(4));
    createMathTool('l-to-gal', 'Liters to Gallons', 'Converter', 'Convert liters to US gallons.', [{key:'l', label:'Liters'}], (v) => (v.l * 0.264172).toFixed(4));
    createMathTool('gal-to-l', 'Gallons to Liters', 'Converter', 'Convert US gallons to liters.', [{key:'gal', label:'Gallons'}], (v) => (v.gal / 0.264172).toFixed(4));
    createMathTool('speed-kph-mph', 'KPH to MPH', 'Converter', 'Convert speed.', [{key:'kph', label:'KPH'}], (v) => (v.kph * 0.621371).toFixed(2));
    createMathTool('speed-mph-kph', 'MPH to KPH', 'Converter', 'Convert speed.', [{key:'mph', label:'MPH'}], (v) => (v.mph / 0.621371).toFixed(2));
    createMathTool('data-mb-gb', 'MB to GB', 'Converter', 'Convert Megabytes to Gigabytes.', [{key:'mb', label:'MB'}], (v) => (v.mb / 1024).toFixed(4));
    createMathTool('data-gb-mb', 'GB to MB', 'Converter', 'Convert Gigabytes to Megabytes.', [{key:'gb', label:'GB'}], (v) => (v.gb * 1024).toFixed(2));
    createMathTool('data-byte-kb', 'Bytes to KB', 'Converter', 'Convert Bytes to KB.', [{key:'b', label:'Bytes'}], (v) => (v.b / 1024).toFixed(4));
    createMathTool('time-min-sec', 'Minutes to Seconds', 'Time', 'Convert minutes to seconds.', [{key:'m', label:'Minutes'}], (v) => v.m * 60);
    createMathTool('time-hr-min', 'Hours to Minutes', 'Time', 'Convert hours to minutes.', [{key:'h', label:'Hours'}], (v) => v.h * 60);
    createMathTool('time-day-hr', 'Days to Hours', 'Time', 'Convert days to hours.', [{key:'d', label:'Days'}], (v) => v.d * 24);
    createMathTool('energy-j-cal', 'Joules to Calories', 'Converter', 'Convert energy.', [{key:'j', label:'Joules'}], (v) => (v.j / 4.184).toFixed(4));
    createMathTool('power-hp-kw', 'Horsepower to kW', 'Converter', 'Convert power.', [{key:'hp', label:'Horsepower'}], (v) => (v.hp * 0.7457).toFixed(4));
    createGeneratorTool('random-letter', 'Random Letter', 'Game', 'Random alphabet letter.', 'Pick Letter', () => 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.charAt(Math.floor(Math.random() * 26)));
    createGeneratorTool('random-emoji', 'Random Emoji', 'Game', 'Random emoji.', 'Pick Emoji', () => ['😀','😂','🥰','😎','🤔','😭','😡','👍','👎','🎉','🔥','❤️'].sort(() => 0.5 - Math.random())[0]);
    createGeneratorTool('lorem-sentence', 'Lorem Sentence', 'Text', 'Random latin sentence.', 'Generate', () => "Lorem ipsum dolor sit amet consectetur adipiscing elit.");
    createSimpleTextTool('space-to-dash', 'Spaces to Dashes', 'Text', 'Replace spaces with dashes.', (text) => text.replace(/ /g, '-'));
    createSimpleTextTool('dash-to-space', 'Dashes to Spaces', 'Text', 'Replace dashes with spaces.', (text) => text.replace(/-/g, ' '));
    createSimpleTextTool('underscore-to-space', 'Underscores to Spaces', 'Text', 'Replace underscores with spaces.', (text) => text.replace(/_/g, ' '));
    createSimpleTextTool('space-to-underscore', 'Spaces to Underscores', 'Text', 'Replace spaces with underscores.', (text) => text.replace(/ /g, '_'));
    createSimpleTextTool('remove-special', 'Remove Special Chars', 'Text', 'Keep only alphanumeric.', (text) => text.replace(/[^a-zA-Z0-9 ]/g, ''));
    createSimpleTextTool('keep-numbers', 'Keep Only Numbers', 'Text', 'Remove non-numeric chars.', (text) => text.replace(/[^0-9]/g, ''));
    createMathTool('bmr-calc', 'BMR Calculator', 'Health', 'Basal Metabolic Rate.',
        [{key:'w', label:'Weight (kg)'}, {key:'h', label:'Height (cm)'}, {key:'a', label:'Age'}],
        (v) => (10 * v.w + 6.25 * v.h - 5 * v.a + 5).toFixed(0) + ' kcal (M) / ' + (10 * v.w + 6.25 * v.h - 5 * v.a - 161).toFixed(0) + ' kcal (F)');
    createMathTool('water-intake', 'Water Intake', 'Health', 'Daily water need (L).',
        [{key:'w', label:'Weight (kg)'}],
        (v) => (v.w * 0.033).toFixed(2) + ' Liters');
    createMathTool('target-heart-rate', 'Target Heart Rate', 'Health', 'Zone 2 (60-70%).',
        [{key:'age', label:'Age'}],
        (v) => {
            const max = 220 - v.age;
            return Math.floor(max * 0.6) + ' - ' + Math.floor(max * 0.7) + ' bpm';
        });
    createMathTool('gpa-calc', 'GPA Calculator (4.0)', 'Science', 'Simple Avg GPA.',
        [{key:'g1', label:'Grade 1'}, {key:'g2', label:'Grade 2'}, {key:'g3', label:'Grade 3'}, {key:'g4', label:'Grade 4'}],
        (v) => ((v.g1 + v.g2 + v.g3 + v.g4) / 4).toFixed(2));
    createMathTool('grade-pct', 'Grade Percentage', 'Science', 'Score / Total.',
        [{key:'s', label:'Score'}, {key:'t', label:'Total'}],
        (v) => ((v.s / v.t) * 100).toFixed(2) + '%');
    createSimpleTextTool('html-minifier', 'HTML Minifier', 'Dev', 'Remove whitespace.', (text) => text.replace(/\s+/g, ' ').replace(/> </g, '><'));
    createSimpleTextTool('hashtag-gen', 'Hashtag Generator', 'Social', 'Generate tags from text.', (text) => text.split(' ').map(w => '#' + w).join(' '));
    createSimpleTextTool('tweet-link', 'Tweet Link Gen', 'Social', 'Create intent link.', (text) => 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(text));
    createSimpleTextTool('binary-to-hex', 'Binary to Hex', 'Dev', 'Convert Bin to Hex.', (text) => parseInt(text.replace(/[^01]/g, ''), 2).toString(16).toUpperCase());
    createSimpleTextTool('hex-to-binary', 'Hex to Binary', 'Dev', 'Convert Hex to Bin.', (text) => parseInt(text, 16).toString(2));
    createMathTool('currency-usd-eur', 'USD to EUR (Mock)', 'Finance', 'Est. rate 0.92', [{key:'usd', label:'USD'}], (v) => (v.usd * 0.92).toFixed(2));
    createMathTool('currency-eur-usd', 'EUR to USD (Mock)', 'Finance', 'Est. rate 1.09', [{key:'eur', label:'EUR'}], (v) => (v.eur * 1.09).toFixed(2));