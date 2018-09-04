import numpy as np

def gt_list_to_gt_dict(gt):
    gt_mapping = dict()
    for query_i,doc_i in gt:
        if query_i in gt_mapping.keys():
            gt_mapping[query_i].append(doc_i)
        else:
            gt_mapping[query_i] = [doc_i]

    return gt_mapping
def relevance_feedback(vec_docs, vec_queries, sim, gt, n=10):
    """
    relevance feedback
    Parameters
        ----------
        vec_docs: sparse array,
            tfidf vectors for documents. Each row corresponds to a document.
        vec_queries: sparse array,
            tfidf vectors for queries. Each row corresponds to a document.
        sim: numpy array,
            matrix of similarities scores between documents (rows) and queries (columns)
        n: integer
            number of documents to assume relevant/non relevant

    Returns
    -------
    rf_sim : numpy array
        matrix of similarities scores between documents (rows) and updated queries (columns)
    """

    # print np.argsort(-sim[:, 0])[:6]
    gt_mapping = gt_list_to_gt_dict(gt)

    alpha=0.75
    beta=0.15

    updated_queries = vec_queries.copy()

    for index,query in enumerate(vec_queries):
        top_n_docs_index = np.argsort(-sim[:, index])[:n]
        relevent_docs_index = [x for x in top_n_docs_index if x in gt_mapping[index+1]]
        non_relevent_docs_index = list(set(top_n_docs_index)-set(relevent_docs_index))
        relevent_docs = vec_docs[relevent_docs_index]
        non_relevent_docs=vec_docs[non_relevent_docs_index]
        update_factor = np.subtract(alpha*np.mean(relevent_docs,axis=0), beta*np.mean(non_relevent_docs,axis=0))
        print "================================="
        print update_factor.shape



    rf_sim = sim # change
    return rf_sim


def relevance_feedback_exp(vec_docs, vec_queries, sim, tfidf_model, n=10):
    """
    relevance feedback with expanded queries
    Parameters
        ----------
        vec_docs: sparse array,
            tfidf vectors for documents. Each row corresponds to a document.
        vec_queries: sparse array,
            tfidf vectors for queries. Each row corresponds to a document.
        sim: numpy array,
            matrix of similarities scores between documents (rows) and queries (columns)
        tfidf_model: TfidfVectorizer,
            tf_idf pretrained model
        n: integer
            number of documents to assume relevant/non relevant

    Returns
    -------
    rf_sim : numpy array
        matrix of similarities scores between documents (rows) and updated queries (columns)
    """

    rf_sim = sim  # change
    return rf_sim