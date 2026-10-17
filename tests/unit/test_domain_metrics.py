from qwen_domain.metrics import metrics

def test_critical_false_negative_counts_abstention_as_miss():
    m=metrics(['YES','YES','NO','NO','UNKNOWN'],['YES','UNKNOWN','YES','NO','UNKNOWN'],'share_blocking')
    assert m['positive_recall']==.5 and m['positive_false_negatives']==1 and m['positive_false_positives']==1
    assert m['negative_precision']==1 and m['negative_recall_specificity']==.5
    assert m['per_class']['UNKNOWN']['support']==1 and m['per_class']['UNKNOWN']['precision']==.5

def test_deadline_has_real_positive_and_negative_labels():
    m=metrics(['PASSED','OPEN','UNKNOWN'],['OPEN','OPEN','UNKNOWN'],'deadline_status')
    assert m['positive_label']=='PASSED' and m['positive_support']==1 and m['positive_false_negatives']==1
    assert m['negative_label']=='OPEN' and m['negative_precision']==.5
