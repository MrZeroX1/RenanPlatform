from ibm_watsonx_ai.foundation_models import Model

def get_credentials():
	return {
		"url" : "https://eu-de.ml.cloud.ibm.com",
		"apikey" : "B50IFqeVP1KrX1rBCnaDQqdVpEDd_ZkxxLFdPKioWZuD"
	}

project_id = "dfecab4f-ecf4-44ab-999d-1e5a330df2fb"
model_id = "sdaia/allam-1-13b-instruct"

parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 200,
    "repetition_penalty": 1,
	"stop_sequences": ["\n"]
}

model = Model(
	model_id = model_id,
	params = parameters,
	credentials = get_credentials(),
	project_id = project_id,
	)

prompt_input = """Arabic Saudi Content Generation

Input: كتب إعلان ترويجي عن مشروب قهوة باردة بلهجة نجدية لجذب الشباب في أيام الصيف الحارة، موضحًا الفوائد والجو العام في المقهى.
Output: قَهْوَة بَارِدَة تْنَعِش قَلْبَك وَتْبَرِّد عَلَيك حَرّ الصَّيف! تَعَال جَرِّب الطَّعْم اللِّي يْرَوِّقك وَيْخَلِّيك تْحِسّ بِالإِنْتِعَاش فِي جَو مَرِيح وَهَادِئ. خُذ قَهْوَتَك وَاسْتَمْتِع بِيُومَك.

Input: سوي إعلان تفصيلي لخدمة حلاقة متنقلة بلهجة قطيفية، يبرز الراحة وسهولة الخدمة، ويخاطب الأشخاص اللي يفضلون الراحة في منازلهم.
Output: مَا تْحْتَاج تِتْحَرَّك مِن مَكَانَك، الحَلَاقَة تْجِيك عِنْد بَاب بَيْتَك! احْنَا نْوَفِّر لَك الرَّاحَة بِخِدْمَة سَرِيعَة وَمُمَيَّزَة.

Input: كتب إعلان ترويجي لتطبيق تسوّق إلكتروني بلهجة سعودية حديثة، يشجع الناس على الاستفادة من التوصيل السريع والعروض المميزة.
Output: كُلّ اللِّي تْحْتَاجَه بْضَغْطَة زِرّ! جَرِّب تَطْبِيقْنَا وَخَلّك أَوَّل مَنْ يْحْصَل عَلَى العُرُوض وَالتَّخْفِيضَات. حَمِّل التَّطْبِيق وَاسْتَمْتِع بِالتَّسَوُّق.

Input: اعمل إعلان إبداعي لمنتج جديد للعناية بالبشرة بلهجة نجدية، يستهدف الشباب اللي يحبون يعتنون ببشرتهم ويظهرون بإطلالة مشرقة.
Output: مُنْتَجْنَا لِلْعِنَايَة بِالبَشْرَة يْعْطِيك إِشْرَاقَة طَبِيعِيَّة. جَرِّبُوه لِبَشْرَة نَضْرَة وَثِقُوا فِي كُلّ يَوْم!

Input: اكتب إعلان عن افتتاح مطعم جديد بلهجة قطيفية، يخاطب العائلات اللي تحب تجربة الأطباق الجديدة وأجواء المطاعم.
Output: جَرِّبُوا مَطْعَمْنَا الجَدِيد، أَطْبَاق لَذِيذَة وَأَجْوَاء رَائِعَة. تَعَالُوا مَع العَائِلَة وَعِيشُوا تَجْرِبَة مُمَيَّزَة.

Input: اكتب إعلان لخدمة توصيل هدايا بلهجة سعودية حديثة، يستهدف الأفراد اللي يبحثون عن خدمة مميزة لتوصيل الهدايا في المناسبات الخاصة.
Output: خَلّ مُنَاسَبَتَك تْكُون أَحْلَى مَع خِدْمَة تَوْصِيل الهَدَايَا! اطْلُب هَدِيَّتَك وَخَلِّنَا نْوَصِّلَهَا لَك بْكُلّ حُبّ.

Input: اكتب إعلان عن معرض سيارات فاخرة بلهجة نجدية، يستقطب عشاق السيارات ويبرز الفخامة في المعرض.
Output: مَعْرَضنَا يِجْمَع أَفْخَر السَّيَّارَات لِلْمُحِبِّين. تَعَال وَشُوف الفَخَامَة عَنْ قُرْب فِي أَحْدَث الطِّرَازَات.

Input: اكتب إعلان لخدمة تأجير قاعات مناسبات بلهجة قطيفية، يستهدف الأزواج اللي يخططون لحفلات زواجهم ويبحثون عن خدمة راقية.
Output: يُوم زَوَاجِك خَاصّ، وَاحْنَا نْوَفِّر لَك قَاعَات مُمَيَّزَة لِأَجْمَل لَحَظَات. احْجِز القَاعَة اليُوم وَخَلِّنَا نْرَتِّب لَكُم كُلّ شَيْ.

Input: سوي إعلان لمنصة تعليمية بلهجة سعودية حديثة، تستهدف الطلاب اللي يبحثون عن طرق تعليم جديدة وعصرية.
Output: التَّعْلِيم صَار أَسْهَل مَع مَنْصَّتْنَا! انْضَمّ لْنَا وَتَعَلَّم بْكُل رَاحَة وَفِي وَقْتَك.

Input: اكتب إعلان لمركز رياضي بلهجة نجدية، يستقطب محبي اللياقة اللي يحرصون على صحتهم ورشاقتهم.
Output: لَكُلّ الّي يْهْتَم بِلِيَاقَتِه، مَرْكَزْنَا يْقَدِّم أَحْدَث التَّجْهِيزَات. تَعَال وَابْدَأ رِحْلَتَك لِصِحَّة أَفْضَل.

Input: اكتب إعلان ترويجي عن مشروب منعش بلهجة نجدية، يستهدف الناس في الأيام الحارة.
Output: المشروب اللِّي يْنَسِّيك حَرّ الصَّيف! جَرِّب طَعْم الانتعاش اللِّي مَا تِلْقَاه غَيْر عِنْدِنَا. بَارِد، لَذِيذ، وَجَاهِز يْبَرِّد عَلَيك.

Input: اكتب إعلان لخدمة تصوير مناسبات بلهجة قطيفية، يناسب الأشخاص اللي يحبون توثيق لحظات خاصة.
Output: مَع خِدْمَة التَّصْوِير مَالْنَا، تْصِير لَحَظَاتَك خَالِدَة. احْجِز اليُوم وَدَعْنَا نْوَثِّق أَحْلَى ذِكْرَيَاتَك.

Input: اكتب إعلان ترويجي لمتجر إلكتروني بلهجة سعودية حديثة، يشجع على التسوق السهل والسريع.
Output: تْبِي تْسَوَّق بِكُلّ سُهُولَة؟ تَسَوَّق عَنْ طَرِيق تَطْبِيقْنَا، وْخَلّ العُرُوض وَاصِلَة عِنْدَك بِكِلَاك ضَغْطَة.

Input: اعمل إعلان عن كريم واقي من الشمس بلهجة نجدية، يستهدف الناس اللي يحبون يحمون بشرتهم.
Output: كْرِيم الوِقَايَة اللِّي يْحْمِيك مِن شَمْس الصَّيف. سَهْل التَّطْبِيق وَيْعْطِيك حِمَايَة طُول اليُوم.

Input: اكتب إعلان عن مطعم مأكولات بحرية بلهجة قطيفية، يناسب العائلات اللي تحب الأكل البحري.
Output: فِي مَطْعَمْنَا، أَفْرَشْنَا لَكُم الطَّاوِلَة بِأَطْيَب أَكْلَات بَحْرِيَّة. تَعَالُوا جَرِّبُوا لَذَّتْنَا بِيَدْنَا.

Input: اكتب إعلان توصيل الهدايا بلهجة سعودية حديثة، يبرز الخدمة المميزة والتوصيل السريع.
Output: وَدِّهَدِيَّتَك فِي وَقْتَك! خِدْمَة تَوْصِيل مُبَاشَر، بْكُلّ حُبّ وَدِقَّة. اطْلُب اليُوم وَدَعْنَا نْوَصِّل فَرْحَتَك."


Input: اكتب إعلان عن معرض تصوير بلهجة نجدية، يستقطب عشاق الصور ويوضح الفعالية.
Output: مَعْرَض التَّصْوِير اللِّي يْجْمَع كُلّ جَمَال الصُّور فِي مَكَان وَاحِد. زُورُونَا وَعِيشُوا التَّجْرِبَة بْنَفْسَكُم.

Input: اكتب إعلان عن تأجير كوشات أفراح بلهجة قطيفية، يناسب الأزواج اللي يخططون للزواج.
Output: خَلّ لَيْلَتَكُم مُمَيِّزَة مَع كُوشَاتْنَا الخَاصَّة. احْجِزُوا اليُوم وَتَأَلَّقُوا بِيَلِيلَتْكُم.

Input: سوي إعلان لمنصة تعليمية بلهجة سعودية حديثة، يبرز سهولة الوصول والدروس المتنوعة.
Output: تَعَلَّم بْرَاحَتَك وَفِي وَقْتَك! مَنْصَّتْنَا فِيهَا دُرُوس لِكُلّ مَجَال، جَرِّبْهَا اليُوم.

Input: اكتب إعلان عن نادي رياضي بلهجة نجدية، يستقطب اللي يهتمون بلياقتهم.
Output: نَادِينَا يْجَهَّز لَك أَفْضَل الأَجْهِزَة وَالتَّمَارِين. خَلّ اللِّيَاقَة جُزْء مِن حَيَاتِك.

Input: اكتب لي اعلان لمقهى راوند بالقطيف بلهجة قطيفية مع العلم ان المقهى يحتوي على العاب ورقية ولوحية ومتنوع ومريح ومتسع الحجم ويفتح 24 ساعة
Output:"""

print("Submitting generation request...")
generated_response = model.generate_text(prompt=prompt_input)
print(generated_response)