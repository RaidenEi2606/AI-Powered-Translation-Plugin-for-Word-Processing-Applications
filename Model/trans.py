from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Bật CORS

# app = Flask(__name__)

# Load mô hình & tokenizer
model_name = "facebook/nllb-200-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Chuyển mô hình sang GPU nếu có
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Lấy danh sách ngôn ngữ hỗ trợ
supported_languages = tokenizer.additional_special_tokens
language_map = {
    'Acehese (Arabic script)': 'ace_Arab',
    'Acehese (Latin script)': 'ace_Latn',
    'Central Moroccan Tamazight (Arabic script)': 'acm_Arab',
    'Algerian Arabic (Arabic script)': 'acq_Arab',
    'Tunisian Arabic (Arabic script)': 'aeb_Arab',
    'Afrikaans': 'afr_Latn',
    'Western Algerian Arabic (Arabic script)': 'ajp_Arab',
    'Akan': 'aka_Latn',
    'Amharic': 'amh_Ethi',
    'Chadian Arabic (Arabic script)': 'apc_Arab',
    'Arabic': 'arb_Arab',
    'Najdi Arabic (Arabic script)': 'ars_Arab',
    'Rifian Arabic (Arabic script)': 'ary_Arab',
    'Egyptian Arabic (Arabic script)': 'arz_Arab',
    'Assamese': 'asm_Beng',
    'Asturian': 'ast_Latn',
    'Awadhi': 'awa_Deva',
    'Aymara': 'ayr_Latn',
    'South Azerbaijani (Arabic script)': 'azb_Arab',
    'Azerbaijani': 'azj_Latn',
    'Bashkir': 'bak_Cyrl',
    'Bambara': 'bam_Latn',
    'Balinese': 'ban_Latn',
    'Belarusian': 'bel_Cyrl',
    'Bemba': 'bem_Latn',
    'Bengali': 'ben_Beng',
    'Bhojpuri': 'bho_Deva',
    'Banjar (Arabic script)': 'bjn_Arab',
    'Banjar (Latin script)': 'bjn_Latn',
    'Tibetan': 'bod_Tibt',
    'Bosnian': 'bos_Latn',
    'Buginese': 'bug_Latn',
    'Bulgarian': 'bul_Cyrl',
    'Catalan': 'cat_Latn',
    'Cebuano': 'ceb_Latn',
    'Czech': 'ces_Latn',
    'CJK (Common Language)': 'cjk_Latn',
    'Central Kurdish (Arabic script)': 'ckb_Arab',
    'Crimean Tatar': 'crh_Latn',
    'Welsh': 'cym_Latn',
    'Danish': 'dan_Latn',
    'German': 'deu_Latn',
    'Digo': 'dik_Latn',
    'Dyula': 'dyu_Latn',
    'Dzongkha': 'dzo_Tibt',
    'Greek': 'ell_Grek',
    'English': 'eng_Latn',
    'Esperanto': 'epo_Latn',
    'Estonian': 'est_Latn',
    'Basque': 'eus_Latn',
    'Ewe': 'ewe_Latn',
    'Faroese': 'fao_Latn',
    'Persian (Arabic script)': 'pes_Arab',
    'Fijian': 'fij_Latn',
    'Finnish': 'fin_Latn',
    'Fon': 'fon_Latn',
    'French': 'fra_Latn',
    'Friulian': 'fur_Latn',
    'Fulah': 'fuv_Latn',
    'Scottish Gaelic': 'gla_Latn',
    'Irish': 'gle_Latn',
    'Galician': 'glg_Latn',
    'Guaraní': 'grn_Latn',
    'Gujarati': 'guj_Gujr',
    'Haitian Creole': 'hat_Latn',
    'Hausa': 'hau_Latn',
    'Hebrew': 'heb_Hebr',
    'Hindi': 'hin_Deva',
    'Chhattisgarhi': 'hne_Deva',
    'Croatian': 'hrv_Latn',
    'Hungarian': 'hun_Latn',
    'Armenian': 'hye_Armn',
    'Igbo': 'ibo_Latn',
    'Ilocano': 'ilo_Latn',
    'Indonesian': 'ind_Latn',
    'Icelandic': 'isl_Latn',
    'Italian': 'ita_Latn',
    'Javanese': 'jav_Latn',
    'Japanese': 'jpn_Jpan',
    'Kabyle': 'kab_Latn',
    'Kayin': 'kac_Latn',
    'Kamba': 'kam_Latn',
    'Kannada': 'kan_Knda',
    'Kashmiri (Arabic script)': 'kas_Arab',
    'Kashmiri (Devanagari script)': 'kas_Deva',
    'Georgian': 'kat_Geor',
    'Northern Kurdish (Arabic script)': 'knc_Arab',
    'Northern Kurdish (Latin script)': 'knc_Latn',
    'Kazakh': 'kaz_Cyrl',
    'Kabiyè': 'kbp_Latn',
    'Cape Verdean Creole': 'kea_Latn',
    'Khmer': 'khm_Khmr',
    'Kikuyu': 'kik_Latn',
    'Kinyarwanda': 'kin_Latn',
    'Kirghiz': 'kir_Cyrl',
    'Kimbundu': 'kmb_Latn',
    'Kongo': 'kon_Latn',
    'Korean': 'kor_Hang',
    'Kurdish': 'kmr_Latn',
    'Lao': 'lao_Laoo',
    'Latvian': 'lvs_Latn',
    'Ligurian': 'lij_Latn',
    'Limburgish': 'lim_Latn',
    'Lingala': 'lin_Latn',
    'Lithuanian': 'lit_Latn',
    'Lombard': 'lmo_Latn',
    'Latgalian': 'ltg_Latn',
    'Luxembourgish': 'ltz_Latn',
    'Luba-Katanga': 'lua_Latn',
    'Luganda': 'lug_Latn',
    'Luo': 'luo_Latn',
    'Mizo': 'lus_Latn',
    'Magahi': 'mag_Deva',
    'Maithili': 'mai_Deva',
    'Malayalam': 'mal_Mlym',
    'Marathi': 'mar_Deva',
    'Minangkabau': 'min_Latn',
    'Macedonian': 'mkd_Cyrl',
    'Piedmontese': 'plt_Latn',
    'Maltese': 'mlt_Latn',
    'Manipuri': 'mni_Beng',
    'Khakas': 'khk_Cyrl',
    'Mossi': 'mos_Latn',
    'Māori': 'mri_Latn',
    'Malay': 'zsm_Latn',
    'Burmese': 'mya_Mymr',
    'Dutch': 'nld_Latn',
    'Norwegian Nynorsk': 'nno_Latn',
    'Norwegian Bokmål': 'nob_Latn',
    'Nepali': 'npi_Deva',
    'Northern Sotho': 'nso_Latn',
    'Nuer': 'nus_Latn',
    'Nyanja': 'nya_Latn',
    'Occitan': 'oci_Latn',
    'Ganda': 'gaz_Latn',
    'Odia': 'ory_Orya',
    'Pangasinan': 'pag_Latn',
    'Punjabi (Gurmukhi script)': 'pan_Guru',
    'Papiamento': 'pap_Latn',
    'Polish': 'pol_Latn',
    'Portuguese': 'por_Latn',
    'Dari': 'prs_Arab',
    'Pashto': 'pbt_Arab',
    'Quechua': 'quy_Latn',
    'Romanian': 'ron_Latn',
    'Rundi': 'run_Latn',
    'Russian': 'rus_Cyrl',
    'Sango': 'sag_Latn',
    'Sanskrit': 'san_Deva',
    'Santali': 'sat_Beng',
    'Sicilian': 'scn_Latn',
    'Shan': 'shn_Mymr',
    'Sinhala': 'sin_Sinh',
    'Slovak': 'slk_Latn',
    'Slovenian': 'slv_Latn',
    'Samoan': 'smo_Latn',
    'Shona': 'sna_Latn',
    'Sindhi': 'snd_Arab',
    'Somali': 'som_Latn',
    'Sotho': 'sot_Latn',
    'Spanish': 'spa_Latn',
    'Albanian': 'als_Latn',
    'Sardinian': 'srd_Latn',
    'Serbian': 'srp_Cyrl',
    'Swazi': 'ssw_Latn',
    'Sundanese': 'sun_Latn',
    'Swedish': 'swe_Latn',
    'Swahili': 'swh_Latn',
    'Silesian': 'szl_Latn',
    'Tamil': 'tam_Taml',
    'Tatar': 'tat_Cyrl',
    'Telugu': 'tel_Telu',
    'Tajik': 'tgk_Cyrl',
    'Tagalog': 'tgl_Latn',
    'Thai': 'tha_Thai',
    'Tigrinya': 'tir_Ethi',
    'Tamazight': 'taq_Latn',
    'Tamazight (Tifinagh script)': 'taq_Tfng',
    'Tok Pisin': 'tpi_Latn',
    'Tswana': 'tsn_Latn',
    'Tsonga': 'tso_Latn',
    'Turkmen': 'tuk_Latn',
    'Tumbuka': 'tum_Latn',
    'Turkish': 'tur_Latn',
    'Twi': 'twi_Latn',
    'Central Atlas Tamazight': 'tzm_Tfng',
    'Uyghur (Arabic script)': 'uig_Arab',
    'Ukrainian': 'ukr_Cyrl',
    'Umbundu': 'umb_Latn',
    'Urdu': 'urd_Arab',
    'Uzbek': 'uzn_Latn',
    'Venetian': 'vec_Latn',
    'Vietnamese': 'vie_Latn',
    'Waray': 'war_Latn',
    'Wolof': 'wol_Latn',
    'Xhosa': 'xho_Latn',
    'Yiddish': 'ydd_Hebr',
    'Yoruba': 'yor_Latn',
    'Cantonese': 'yue_Hant',
    'Chinese (Simplified)': 'zho_Hans',
    'Chinese (Traditional)': 'zho_Hant',
    'Zulu': 'zul_Latn'
}


@app.route("/translate", methods=["POST"])
def translate_text():
    """API nhận dữ liệu JSON và trả về bản dịch"""
    data = request.json
    text = data.get("text", "")
    source_lang_name = data.get("source_lang", "")
    target_lang_name = data.get("target_lang", "")

    # Chuyển đổi tên ngôn ngữ thành language_id
    source_lang = language_map.get(source_lang_name)
    target_lang = language_map.get(target_lang_name)
    print(source_lang,' ',target_lang)
     # ----------------------------------------------------------------
    # Kiểm tra nếu ngôn ngữ không được hỗ trợ
    if source_lang not in supported_languages or target_lang not in supported_languages:
        return jsonify({"error": f"Ngôn ngữ không được hỗ trợ: {source_lang_name} → {target_lang_name}"}), 400
    
    # Định dạng văn bản đầu vào
    text = f"{target_lang} {text}"
    inputs = tokenizer(text, return_tensors="pt").to(device)

    # Lấy ID của mã ngôn ngữ đích
    target_lang_id = tokenizer.convert_tokens_to_ids([target_lang])[0]

    # Dịch văn bản
    translated_tokens = model.generate(**inputs, forced_bos_token_id=target_lang_id)
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    print(translated_text)
    return jsonify({"translated_text": translated_text})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)
