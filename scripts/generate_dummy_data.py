from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

random.seed(42)

OUT_DIR = Path("data/raw/synthetic")
SOURCES = ["sms", "email", "chat"]
DEFAULT_SAMPLES_PER_CLASS_PER_SOURCE = 8

BRANDS = ["SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB", "BOB", "Paytm", "PhonePe", "GPay", "Airtel", "Jio"]
UPI_IDS = ["user@upi", "pay@okicici", "name@oksbi", "pay@okhdfc", "txn@okaxis"]
AMOUNTS = ["₹199", "₹499", "₹1,250", "₹2,999", "₹5,000", "₹8,750", "₹12,000"]
TIMES = ["09:15 AM", "10:30 AM", "01:05 PM", "04:40 PM", "07:20 PM"]
DATES = ["13-02-2026", "12-02-2026", "11-02-2026", "10-02-2026", "08-02-2026"]

LANGS: List[Dict[str, object]] = [
    {
        "code": "hi",
        "script": "Devanagari",
        "phish": [
            "आपका {brand} खाता ब्लॉक हो गया है। तुरंत KYC अपडेट करें: {url}",
            "प्रिय ग्राहक, आपका UPI पिन समाप्त होने वाला है। अभी अपडेट करें: {url}",
            "आपके खाते में संदिग्ध लेन-देन {amount} पाया गया। सत्यापन के लिए OTP भेजें।",
            "आपका {brand} कार्ड बंद हो जाएगा। OTP साझा करें।",
            "आपके मोबाइल नंबर पर KYC लंबित है। {url} पर लॉगिन करें।",
            "आपका रिफंड रुका हुआ है। खाते की जानकारी अपडेट करें।",
            "पैन-आधार लिंक असफल। तुरंत {url} पर अपडेट करें।",
            "बैंक चेतावनी: पासवर्ड सत्यापित करें।",
            "आपका अकाउंट 24 घंटे में बंद होगा। पुष्टि करें: {url}",
            "तत्काल कार्रवाई करें, OTP/पिन बताएं।",
        ],
        "benign": [
            "{brand}: आपके खाते से {amount} की निकासी हुई। अगर यह आप नहीं थे तो ग्राहक सेवा से संपर्क करें।",
            "{brand}: {amount} का UPI भुगतान सफल। Txn ID {txn_id}.",
            "आपका OTP {otp} है। इसे किसी के साथ साझा न करें।",
            "आपकी बिल भुगतान रसीद उपलब्ध है।",
            "डिलीवरी अपडेट: आपका पार्सल {delivery_id} आज पहुंचेगा।",
            "आपकी अपॉइंटमेंट {date} को {time} बजे तय है।",
            "आपके खाते में {amount} का क्रेडिट हुआ।",
            "आपका रिचार्ज {amount} सफल रहा।",
            "ट्रांजैक्शन विफल, रकम 2-3 दिन में लौटाई जाएगी।",
            "धन्यवाद, आपकी शिकायत दर्ज हो गई है।",
        ],
    },
    {
        "code": "bn",
        "script": "Bengali",
        "phish": [
            "আপনার {brand} অ্যাকাউন্ট স্থগিত করা হয়েছে। এখনই KYC আপডেট করুন: {url}",
            "UPI পিন মেয়াদ শেষ। আপডেট করুন: {url}",
            "সন্দেহজনক লেনদেন {amount} ধরা পড়েছে। যাচাইয়ের জন্য OTP দিন।",
            "আপনার কার্ড ব্লক হবে। OTP শেয়ার করুন।",
            "রিফান্ড আটকে আছে। তথ্য আপডেট করুন।",
            "প্যান-আধার লিংক ব্যর্থ। {url} এ আপডেট করুন।",
            "অ্যাকাউন্ট ২৪ ঘণ্টায় বন্ধ হবে। নিশ্চিত করুন: {url}",
            "পাসওয়ার্ড যাচাই করতে হবে।",
            "গ্রাহক, আপনার নম্বর KYC বাকি।",
            "জরুরি, PIN জানান।",
        ],
        "benign": [
            "{brand}: আপনার অ্যাকাউন্ট থেকে {amount} ডেবিট হয়েছে।",
            "{brand}: UPI পেমেন্ট সফল {amount}। Txn {txn_id}.",
            "আপনার OTP {otp}। কারও সাথে শেয়ার করবেন না।",
            "ডেলিভারি আপডেট: পার্সেল {delivery_id} আজ পৌঁছাবে।",
            "আপনার অ্যাপয়েন্টমেন্ট {date} {time} এ।",
            "রিচার্জ {amount} সফল।",
            "ব্যর্থ লেনদেন, টাকা ফেরত ২-৩ দিনের মধ্যে।",
            "বিল পেমেন্ট রসিদ প্রস্তুত।",
            "আপনার অভিযোগ নথিভুক্ত হয়েছে।",
            "অ্যাকাউন্টে {amount} ক্রেডিট হয়েছে।",
        ],
    },
    {
        "code": "ta",
        "script": "Tamil",
        "phish": [
            "{brand} கணக்கு முடக்கப்பட்டது. KYC புதுப்பிக்கவும்: {url}",
            "UPI PIN காலாவதி. உடனே புதுப்பிக்கவும்: {url}",
            "சந்தேகமான பரிவர்த்தனை {amount}. சரிபார்ப்பிற்கு OTP அனுப்பவும்.",
            "உங்கள் கார்டு முடங்கும். OTP பகிரவும்.",
            "திருப்பிச் செலுத்தல் நிலுவையில். விவரங்களை புதுப்பிக்கவும்.",
            "PAN-Aadhaar இணைப்பு தோல்வி. {url} இல் புதுப்பிக்கவும்.",
            "கணக்கு 24 மணி நேரத்தில் மூடப்படும். உறுதிப்படுத்தவும்: {url}",
            "கடவுச்சொல் சரிபார்ப்பு தேவை.",
            "உங்கள் KYC நிலுவையில் உள்ளது.",
            "அவசரம், PIN தெரிவிக்கவும்.",
        ],
        "benign": [
            "{brand}: உங்கள் கணக்கில் இருந்து {amount} டெபிட் ஆனது.",
            "{brand}: {amount} UPI பணம் செலுத்தல் வெற்றி. Txn {txn_id}.",
            "உங்கள் OTP {otp}. எவருடனும் பகிர வேண்டாம்.",
            "டெலிவரி அப்டேட்: பார்சல் {delivery_id} இன்று வரும்.",
            "உங்கள் நேர்முகம் {date} {time} அன்று.",
            "ரீசார்ஜ் {amount} வெற்றி.",
            "பரிவர்த்தனை தோல்வி, தொகை 2-3 நாட்களில் திருப்பி வழங்கப்படும்.",
            "பில் கட்டணம் ரசீது தயாராக உள்ளது.",
            "உங்கள் புகார் பதிவு செய்யப்பட்டது.",
            "கணக்கில் {amount} கிரெடிட் ஆனது.",
        ],
    },
    {
        "code": "te",
        "script": "Telugu",
        "phish": [
            "{brand} ఖాతా నిలిపివేయబడింది. KYC అప్‌డేట్ చేయండి: {url}",
            "UPI పిన్ గడువు ముగిసింది. వెంటనే అప్‌డేట్ చేయండి: {url}",
            "సందేహాస్పద లావాదేవీ {amount}. ధృవీకరణకు OTP పంపండి.",
            "మీ కార్డ్ బ్లాక్ అవుతుంది. OTP షేర్ చేయండి.",
            "రిఫండ్ నిలిచిపోయింది. వివరాలు అప్‌డేట్ చేయండి.",
            "PAN-Aadhaar లింక్ విఫలమైంది. {url} లో అప్‌డేట్ చేయండి.",
            "ఖాతా 24 గంటల్లో మూసేస్తారు. నిర్ధారించండి: {url}",
            "పాస్‌వర్డ్ ధృవీకరణ అవసరం.",
            "మీ KYC పెండింగ్‌లో ఉంది.",
            "అత్యవసరం, PIN చెప్పండి.",
        ],
        "benign": [
            "{brand}: మీ ఖాతా నుండి {amount} డెబిట్ అయింది.",
            "{brand}: {amount} UPI చెల్లింపు విజయవంతం. Txn {txn_id}.",
            "మీ OTP {otp}. ఎవరికీ చెప్పవద్దు.",
            "డెలివరీ అప్డేట్: పార్సెల్ {delivery_id} ఇవాళ వస్తుంది.",
            "మీ అపాయింట్‌మెంట్ {date} {time}కు.",
            "రిచార్జ్ {amount} విజయవంతం.",
            "లావాదేవీ విఫలం, మొత్తాన్ని 2-3 రోజుల్లో తిరిగి క్రెడిట్ చేస్తారు.",
            "బిల్ చెల్లింపు రసీదు సిద్ధంగా ఉంది.",
            "మీ ఫిర్యాదు నమోదు అయ్యింది.",
            "ఖాతాలో {amount} క్రెడిట్ అయింది.",
        ],
    },
    {
        "code": "mr",
        "script": "Devanagari",
        "phish": [
            "{brand} खाते ब्लॉक केले आहे. KYC अपडेट करा: {url}",
            "UPI पिनची मुदत संपली. ताबडतोब अपडेट करा: {url}",
            "संशयास्पद व्यवहार {amount}. पडताळणीसाठी OTP पाठवा.",
            "तुमचे कार्ड ब्लॉक होईल. OTP शेअर करा.",
            "रिफंड अडकला आहे. माहिती अपडेट करा.",
            "PAN-Aadhaar लिंक अयशस्वी. {url} वर अपडेट करा.",
            "खाते 24 तासांत बंद होईल. पुष्टी करा: {url}",
            "पासवर्ड पडताळणी आवश्यक.",
            "तुमचे KYC प्रलंबित आहे.",
            "तत्काळ PIN सांगा.",
        ],
        "benign": [
            "{brand}: तुमच्या खात्यातून {amount} डेबिट झाले.",
            "{brand}: {amount} UPI पेमेंट यशस्वी. Txn {txn_id}.",
            "तुमचा OTP {otp}. कोणासही सांगू नका.",
            "डिलिव्हरी अपडेट: पार्सल {delivery_id} आज येईल.",
            "तुमची भेट {date} रोजी {time} ला आहे.",
            "रिचार्ज {amount} यशस्वी.",
            "व्यवहार अयशस्वी, रक्कम 2-3 दिवसांत परत येईल.",
            "बिल पेमेंट पावती उपलब्ध.",
            "तुमची तक्रार नोंदवली आहे.",
            "खात्यात {amount} क्रेडिट झाले.",
        ],
    },
    {
        "code": "gu",
        "script": "Gujarati",
        "phish": [
            "{brand} ખાતું બ્લોક થયું છે. KYC અપડેટ કરો: {url}",
            "UPI પિનની મુદત પૂરી થઈ. તરત અપડેટ કરો: {url}",
            "શંકાસ્પદ લેવડદેવડ {amount}. ચકાસણી માટે OTP મોકલો.",
            "તમારો કાર્ડ બ્લોક થશે. OTP શેર કરો.",
            "રિફંડ અટક્યું છે. વિગતો અપડેટ કરો.",
            "PAN-Aadhaar લિંક નિષ્ફળ. {url} પર અપડેટ કરો.",
            "ખાતું 24 કલાકમાં બંધ થશે. પુષ્ટિ કરો: {url}",
            "પાસવર્ડ ચકાસણી જરૂરી.",
            "તમારી KYC પેન્ડિંગ છે.",
            "તાત્કાલિક PIN કહો.",
        ],
        "benign": [
            "{brand}: તમારા ખાતામાંથી {amount} ડેબિટ થયું.",
            "{brand}: {amount} UPI ચુકવણી સફળ. Txn {txn_id}.",
            "તમારો OTP {otp}. કોઈ સાથે શેર ન કરો.",
            "ડિલિવરી અપડેટ: પાર્સલ {delivery_id} આજે આવશે.",
            "તમારો અપોઈન્ટમેન્ટ {date} {time} પર છે.",
            "રીચાર્જ {amount} સફળ.",
            "ટ્રાન્ઝેક્શન નિષ્ફળ, રકમ 2-3 દિવસમાં પાછી આવશે.",
            "બિલ ચુકવણી રસીદ તૈયાર છે.",
            "તમારી ફરિયાદ નોંધાઈ છે.",
            "ખાતામાં {amount} ક્રેડિટ થયું.",
        ],
    },
    {
        "code": "kn",
        "script": "Kannada",
        "phish": [
            "{brand} ಖಾತೆ ತಡೆಹಿಡಿಯಲಾಗಿದೆ. KYC ನವೀಕರಿಸಿ: {url}",
            "UPI ಪಿನ್ ಅವಧಿ ಮುಕ್ತಾಯ. ತಕ್ಷಣ ನವೀಕರಿಸಿ: {url}",
            "ಸಂದೇಹಾಸ್ಪದ ವ್ಯವಹಾರ {amount}. ಪರಿಶೀಲನೆಗೆ OTP ನೀಡಿ.",
            "ನಿಮ್ಮ ಕಾರ್ಡ್ ಬ್ಲಾಕ್ ಆಗಲಿದೆ. OTP ಹಂಚಿ.",
            "ರಿಫಂಡ್ ಅಟಕಿದೆ. ವಿವರಗಳನ್ನು ನವೀಕರಿಸಿ.",
            "PAN-Aadhaar ಲಿಂಕ್ ವಿಫಲ. {url} ನಲ್ಲಿ ನವೀಕರಿಸಿ.",
            "ಖಾತೆ 24 ಗಂಟೆಯಲ್ಲಿ ಮುಚ್ಚಲಾಗುತ್ತದೆ. ದೃಢಪಡಿಸಿ: {url}",
            "ಪಾಸ್ವರ್ಡ್ ಪರಿಶೀಲನೆ ಅಗತ್ಯ.",
            "ನಿಮ್ಮ KYC ಬಾಕಿ ಇದೆ.",
            "ತುರ್ತು, PIN ತಿಳಿಸಿ.",
        ],
        "benign": [
            "{brand}: ನಿಮ್ಮ ಖಾತೆಯಿಂದ {amount} ಡೆಬಿಟ್ ಆಗಿದೆ.",
            "{brand}: {amount} UPI ಪಾವತಿ ಯಶಸ್ವಿ. Txn {txn_id}.",
            "ನಿಮ್ಮ OTP {otp}. ಯಾರೊಂದಿಗೆ ಹಂಚಬೇಡಿ.",
            "ಡೆಲಿವರಿ ಅಪ್ಡೇಟ್: ಪಾರ್ಸಲ್ {delivery_id} ಇಂದು ಬರುತ್ತದೆ.",
            "ನಿಮ್ಮ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ {date} {time} ಕ್ಕೆ.",
            "ರೀಚಾರ್ಜ್ {amount} ಯಶಸ್ವಿ.",
            "ಟ್ರಾನ್ಸಾಕ್ಷನ್ ವಿಫಲ, ಮೊತ್ತ 2-3 ದಿನಗಳಲ್ಲಿ ಹಿಂತಿರುಗುತ್ತದೆ.",
            "ಬಿಲ್ ಪಾವತಿ ರಸೀದಿ ಸಿದ್ಧವಾಗಿದೆ.",
            "ನಿಮ್ಮ ದೂರು ದಾಖಲಾಗಿದೆ.",
            "ಖಾತೆಗೆ {amount} ಕ್ರೆಡಿಟ್ ಆಗಿದೆ.",
        ],
    },
    {
        "code": "ml",
        "script": "Malayalam",
        "phish": [
            "{brand} അക്കൗണ്ട് ബ്ലോക്ക് ചെയ്തു. KYC അപ്‌ഡേറ്റ് ചെയ്യുക: {url}",
            "UPI പിൻ കാലാവധി കഴിഞ്ഞു. ഉടൻ അപ്‌ഡേറ്റ് ചെയ്യുക: {url}",
            "സംശയാസ്പദ ഇടപാട് {amount}. പരിശോധനയ്ക്ക് OTP നൽകുക.",
            "നിങ്ങളുടെ കാർഡ് ബ്ലോക്ക് ചെയ്യും. OTP പങ്കിടുക.",
            "റീഫണ്ട് തടഞ്ഞിരിക്കുന്നു. വിവരങ്ങൾ അപ്‌ഡേറ്റ് ചെയ്യുക.",
            "PAN-Aadhaar ലിങ്ക് പരാജയം. {url} ൽ അപ്‌ഡേറ്റ് ചെയ്യുക.",
            "24 മണിക്കൂറിൽ അക്കൗണ്ട് അടയ്ക്കും. സ്ഥിരീകരിക്കുക: {url}",
            "പാസ്‌വേഡ് സ്ഥിരീകരണം ആവശ്യമാണ്.",
            "നിങ്ങളുടെ KYC ബാക്കി.",
            "അത്യാവശ്യമാണ്, PIN പറയുക.",
        ],
        "benign": [
            "{brand}: നിങ്ങളുടെ അക്കൗണ്ടിൽ നിന്ന് {amount} ഡെബിറ്റ് ചെയ്തു.",
            "{brand}: {amount} UPI പേയ്മെന്റ് വിജയിച്ചു. Txn {txn_id}.",
            "നിങ്ങളുടെ OTP {otp}. ആരോടും പങ്കിടരുത്.",
            "ഡെലിവറി അപ്‌ഡേറ്റ്: പാഴ്സൽ {delivery_id} ഇന്ന് എത്തും.",
            "നിങ്ങളുടെ അപ്പോയിന്റ്മെന്റ് {date} {time} ന്.",
            "റീചാർജ് {amount} വിജയിച്ചു.",
            "ഇടപാട് പരാജയം, തുക 2-3 ദിവസത്തിൽ തിരികെ ലഭിക്കും.",
            "ബിൽ പേയ്മെന്റ് രസീദ് തയ്യാറായി.",
            "നിങ്ങളുടെ പരാതി രജിസ്റ്റർ ചെയ്തു.",
            "അക്കൗണ്ടിൽ {amount} ക്രെഡിറ്റ് ചെയ്തു.",
        ],
    },
    {
        "code": "pa",
        "script": "Gurmukhi",
        "phish": [
            "{brand} ਖਾਤਾ ਬਲੌਕ ਹੋ ਗਿਆ ਹੈ। KYC ਅੱਪਡੇਟ ਕਰੋ: {url}",
            "UPI ਪਿਨ ਦੀ ਮਿਆਦ ਖਤਮ। ਤੁਰੰਤ ਅੱਪਡੇਟ ਕਰੋ: {url}",
            "ਸ਼ੱਕੀ ਲੈਣ-ਦੇਣ {amount}. ਜਾਂਚ ਲਈ OTP ਦਿਓ।",
            "ਤੁਹਾਡਾ ਕਾਰਡ ਬਲੌਕ ਹੋਵੇਗਾ। OTP ਸਾਂਝਾ ਕਰੋ।",
            "ਰਿਫੰਡ ਅਟਕਿਆ ਹੈ। ਵੇਰਵੇ ਅੱਪਡੇਟ ਕਰੋ।",
            "PAN-Aadhaar ਲਿੰਕ ਅਸਫਲ। {url} ਤੇ ਅੱਪਡੇਟ ਕਰੋ।",
            "ਖਾਤਾ 24 ਘੰਟਿਆਂ ਵਿੱਚ ਬੰਦ ਹੋਵੇਗਾ। ਪੁਸ਼ਟੀ ਕਰੋ: {url}",
            "ਪਾਸਵਰਡ ਦੀ ਜਾਂਚ ਲਾਜ਼ਮੀ।",
            "ਤੁਹਾਡੀ KYC ਬਕਾਇਆ ਹੈ।",
            "ਤੁਰੰਤ PIN ਦੱਸੋ।",
        ],
        "benign": [
            "{brand}: ਤੁਹਾਡੇ ਖਾਤੇ ਤੋਂ {amount} ਡੈਬਿਟ ਹੋਇਆ।",
            "{brand}: {amount} UPI ਭੁਗਤਾਨ ਸਫਲ। Txn {txn_id}.",
            "ਤੁਹਾਡਾ OTP {otp} ਹੈ। ਕਿਸੇ ਨਾਲ ਸਾਂਝਾ ਨਾ ਕਰੋ।",
            "ਡਿਲਿਵਰੀ ਅੱਪਡੇਟ: ਪਾਰਸਲ {delivery_id} ਅੱਜ ਆਵੇਗਾ।",
            "ਤੁਹਾਡੀ ਮੀਟਿੰਗ {date} ਨੂੰ {time} ਤੇ ਹੈ।",
            "ਰੀਚਾਰਜ {amount} ਸਫਲ।",
            "ਲੈਣ-ਦੇਣ ਅਸਫਲ, ਰਕਮ 2-3 ਦਿਨਾਂ ਵਿੱਚ ਵਾਪਸ ਆਵੇਗੀ।",
            "ਬਿਲ ਭੁਗਤਾਨ ਰਸੀਦ ਤਿਆਰ ਹੈ।",
            "ਤੁਹਾਡੀ ਸ਼ਿਕਾਇਤ ਦਰਜ ਹੋ ਗਈ ਹੈ।",
            "ਖਾਤੇ ਵਿੱਚ {amount} ਕਰੇਡਿਟ ਹੋਇਆ।",
        ],
    },
    {
        "code": "or",
        "script": "Odia",
        "phish": [
            "{brand} ଖାତା ବ୍ଲକ୍ ହୋଇଛି। KYC ଅପଡେଟ୍ କରନ୍ତୁ: {url}",
            "UPI ପିନ୍ ମেয়ାଦ ସମାପ୍ତ। ତୁରନ୍ଟ ଅପଡେଟ୍ କରନ୍ତୁ: {url}",
            "ସନ୍ଦେହାସ୍ପଦ ଟ୍ରାନ୍ଜାକ୍ସନ୍ {amount}. ଯାଞ୍ଚ ପାଇଁ OTP ଦିଅନ୍ତୁ।",
            "ଆପଣଙ୍କ କାର୍ଡ ବ୍ଲକ୍ ହେବ। OTP ସେୟାର୍ କରନ୍ତୁ।",
            "ରିଫଣ୍ଡ ଅଟକିଛି। ବିବରଣୀ ଅପଡେଟ୍ କରନ୍ତୁ।",
            "PAN-Aadhaar ଲିଙ୍କ୍ ବିଫଳ। {url} ରେ ଅପଡେଟ୍ କରନ୍ତୁ।",
            "ଖାତା 24 ଘଣ୍ଟାରେ ବନ୍ଦ ହେବ। ନିଶ୍ଚିତ କରନ୍ତୁ: {url}",
            "ପାସୱର୍ଡ ଯାଞ୍ଚ ଆବଶ୍ୟକ।",
            "ଆପଣଙ୍କ KYC ପେଣ୍ଡିଂ ଅଛି।",
            "ତୁରନ୍ଟ PIN କହନ୍ତୁ।",
        ],
        "benign": [
            "{brand}: ଆପଣଙ୍କ ଖାତାରୁ {amount} ଡେବିଟ୍ ହୋଇଛି।",
            "{brand}: {amount} UPI ପେମେଣ୍ଟ ସଫଳ। Txn {txn_id}.",
            "ଆପଣଙ୍କ OTP {otp}। କାହାକୁ ଶେୟାର୍ କରନ୍ତୁ ନାହିଁ।",
            "ଡିଲିଭେରି ଅପଡେଟ୍: ପାର୍ସେଲ୍ {delivery_id} ଆଜି ପହଞ୍ଚିବ।",
            "ଆପଣଙ୍କ ଆପଏଣ୍ଟମେଣ୍ଟ {date} {time} କୁ।",
            "ରିଚାର୍ଜ {amount} ସଫଳ।",
            "ଟ୍ରାନ୍ଜାକ୍ସନ୍ ବିଫଳ, ଟଙ୍କା 2-3 ଦିନରେ ଫେରିବ।",
            "ବିଲ୍ ପେମେଣ୍ଟ ରସିଦ୍ ପ୍ରସ୍ତୁତ।",
            "ଆପଣଙ୍କ ଅଭିଯୋଗ ରେଜିଷ୍ଟର୍ ହୋଇଛି।",
            "ଖାତାରେ {amount} କ୍ରେଡିଟ୍ ହୋଇଛି।",
        ],
    },
    {
        "code": "ur",
        "script": "Arabic",
        "phish": [
            "{brand} اکاؤنٹ بلاک ہو گیا ہے۔ KYC اپڈیٹ کریں: {url}",
            "UPI پن کی میعاد ختم۔ فوراً اپڈیٹ کریں: {url}",
            "مشکوک لین دین {amount}۔ تصدیق کے لئے OTP دیں۔",
            "آپ کا کارڈ بلاک ہوگا۔ OTP شیئر کریں۔",
            "ریفنڈ رکا ہوا ہے۔ معلومات اپڈیٹ کریں۔",
            "PAN-Aadhaar لنک ناکام۔ {url} پر اپڈیٹ کریں۔",
            "اکاؤنٹ 24 گھنٹوں میں بند ہوگا۔ تصدیق کریں: {url}",
            "پاس ورڈ تصدیق ضروری ہے۔",
            "آپ کی KYC زیر التوا ہے۔",
            "فوری، PIN بتائیں۔",
        ],
        "benign": [
            "{brand}: آپ کے اکاؤنٹ سے {amount} ڈیبٹ ہوا۔",
            "{brand}: {amount} UPI ادائیگی کامیاب۔ Txn {txn_id}.",
            "آپ کا OTP {otp} ہے۔ کسی سے شیئر نہ کریں۔",
            "ڈیلیوری اپڈیٹ: پارسل {delivery_id} آج پہنچے گا۔",
            "آپ کی اپائنٹمنٹ {date} {time} پر ہے۔",
            "ریچارج {amount} کامیاب۔",
            "لین دین ناکام، رقم 2-3 دن میں واپس آ جائے گی۔",
            "بل ادائیگی رسید تیار ہے۔",
            "آپ کی شکایت درج ہو گئی ہے۔",
            "اکاؤنٹ میں {amount} کریڈٹ ہوا۔",
        ],
    },
    {
        "code": "hi-mix",
        "script": "Latin",
        "phish": [
            "{brand} account block ho gaya hai. KYC update karo: {url}",
            "UPI PIN expire ho gaya. Abhi update karo: {url}",
            "Suspicious txn {amount}. Verification ke liye OTP bhejo.",
            "Card block ho jayega. OTP share karo.",
            "Refund pending hai. Details update karo.",
            "PAN-Aadhaar link failed. {url} par update karo.",
            "Account 24 hours me close hoga. Confirm karo: {url}",
            "Password verify karna hoga.",
            "KYC pending hai. Turant update karo.",
            "Urgent, PIN batao.",
        ],
        "benign": [
            "{brand}: {amount} debit hua. Agar aap nahi to helpline se baat karein.",
            "{brand}: {amount} UPI payment successful. Txn {txn_id}.",
            "Your OTP is {otp}. Do not share.",
            "Delivery update: parcel {delivery_id} aaj aayega.",
            "Appointment {date} ko {time} baje hai.",
            "Recharge {amount} successful.",
            "Txn failed, amount 2-3 din me wapas aayega.",
            "Bill payment receipt ready hai.",
            "Complaint register ho gayi hai.",
            "Account me {amount} credit hua.",
        ],
    },
]


def _random_otp() -> str:
    return f"{random.randint(100000, 999999)}"


def _random_phone() -> str:
    return f"{random.randint(6000000000, 9999999999)}"


def _random_txn_id() -> str:
    return f"TXN{random.randint(10000000, 99999999)}"


def _random_delivery_id() -> str:
    return f"DLV{random.randint(100000, 999999)}"


def _random_url(brand: str) -> str:
    slug = brand.lower()
    return f"https://{slug}-secure.in/verify"


def _random_timestamp() -> str:
    base = datetime(2026, 2, 1, 9, 0, 0)
    delta = timedelta(days=random.randint(0, 12), minutes=random.randint(0, 600))
    return (base + delta).isoformat() + "Z"


def _render(text: str) -> Dict[str, str]:
    brand = random.choice(BRANDS)
    payload = {
        "brand": brand,
        "amount": random.choice(AMOUNTS),
        "otp": _random_otp(),
        "url": _random_url(brand),
        "phone": _random_phone(),
        "date": random.choice(DATES),
        "time": random.choice(TIMES),
        "upi": random.choice(UPI_IDS),
        "txn_id": _random_txn_id(),
        "delivery_id": _random_delivery_id(),
    }
    return {
        "text": text.format(**payload),
        "brand": brand,
    }


def generate_samples_for_source(source: str, samples_per_class: int) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for lang in LANGS:
        code = str(lang["code"])
        script = str(lang["script"])
        for label, key in [(1, "phish"), (0, "benign")]:
            templates = list(lang[key])
            for _ in range(samples_per_class):
                template = random.choice(templates)
                rendered = _render(template)
                text = rendered["text"]
                brand = rendered["brand"]
                row = {
                    "id": f"{code}_{source}_{key}_{random.randint(100000, 999999)}",
                    "text": text,
                    "label": label,
                    "language": code,
                    "script": script,
                    "source": source,
                    "timestamp": _random_timestamp(),
                    "intent": "credential" if label == 1 else "none",
                    "url_count": float("http" in text or "www" in text),
                    "phone_count": float("+91" in text),
                    "has_otp_request": bool("OTP" in text or "otp" in text),
                    "brand_mention": brand,
                }
                if source == "email":
                    row["text"] = f"Subject: Important account update\n{row['text']}"
                rows.append(row)
    return rows


def write_manifest(counts: Dict[str, Dict[str, int]]) -> None:
    manifest_path = OUT_DIR / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(counts, f, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--per-class-per-source",
        type=int,
        default=DEFAULT_SAMPLES_PER_CLASS_PER_SOURCE,
        help="Number of samples per class (phish/benign) per language per source.",
    )
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    counts: Dict[str, Dict[str, int]] = {}
    for source in SOURCES:
        rows = generate_samples_for_source(source, samples_per_class=args.per_class_per_source)
        out_path = OUT_DIR / f"{source}.jsonl"
        with open(out_path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False))
                f.write("\n")
        counts[source] = {"total": len(rows), "phish": 0, "benign": 0}
        for row in rows:
            if row["label"] == 1:
                counts[source]["phish"] += 1
            else:
                counts[source]["benign"] += 1
    write_manifest(counts)


if __name__ == "__main__":
    main()
