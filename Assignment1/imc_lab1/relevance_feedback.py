import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
#Not a nice thing to do, but It is needed here..
import warnings
warnings.filterwarnings("ignore")

def gt_list_to_gt_dict(gt):
    gt_mapping = dict()
    for query_i,doc_i in gt:
        if query_i-1 in gt_mapping.keys():
            gt_mapping[query_i-1].append(doc_i-1)
        else:
            gt_mapping[query_i-1] = [doc_i-1]

    return gt_mapping


def vector_adjustment(vec_docs,vec_queries,sim,gt_mapping,n):
    updated_queries = vec_queries.copy()


    alpha=0.75
    beta=0.15


    for index,query in enumerate(vec_queries):
        top_n_docs_index = np.argsort(-sim[:, index])[:n]
        relevent_docs_index = [x for x in top_n_docs_index if x in gt_mapping[index]]
        non_relevent_docs_index = list(set(top_n_docs_index)-set(relevent_docs_index))
        relevent_docs = vec_docs[relevent_docs_index]
        non_relevent_docs=vec_docs[non_relevent_docs_index]
        if len(relevent_docs_index)==0:
            updated_queries[index,:] = np.subtract(query.toarray(), beta*np.mean(non_relevent_docs,axis=0))
        elif len(non_relevent_docs_index)==0:
            updated_queries[index,:] = np.add(query.toarray(),alpha*np.mean(relevent_docs,axis=0))
        else:
            updated_queries[index,:] = np.add(query.toarray(),np.subtract(alpha*np.mean(relevent_docs,axis=0), beta*np.mean(non_relevent_docs,axis=0)))
    
    return updated_queries


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

    gt_mapping = gt_list_to_gt_dict(gt)
    number_of_itr = 3

    while number_of_itr!=0:
        print "iteration left == {}".format(number_of_itr)
        number_of_itr-=1
        updated_queries = vector_adjustment(vec_docs,vec_queries,sim,gt_mapping,n)
        vec_queries = updated_queries
        sim = cosine_similarity(vec_docs, updated_queries)
    
    rf_sim = cosine_similarity(vec_docs, updated_queries)
    return rf_sim


def relevance_feedback_exp(vec_docs, vec_queries, sim, tfidf_model,gt, n=10):
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

    gt_mapping = gt_list_to_gt_dict(gt)

    number_of_itr = 3
    while number_of_itr!=0:
        print "iterations left == {}".format(number_of_itr)
        number_of_itr-=1

        source_queries = vector_adjustment(vec_docs,vec_queries,sim,gt_mapping,n)
        updated_queries = source_queries.copy().toarray()

        for query_index in gt_mapping.keys(): 
            list_of_terms = []
            for doc_index in gt_mapping[query_index]:
                tfidf_vec_of_doc = vec_docs[doc_index].toarray()[0]
                for term_index,term_tfidf in enumerate(tfidf_vec_of_doc):
                    list_of_terms.append((term_tfidf,term_index,doc_index))
            list_of_terms.sort()
            for term_tfidf,term_index,_ in list_of_terms[-n:]:
                updated_queries[query_index][term_index] = term_tfidf
        
        vec_queries = updated_queries
        sim = cosine_similarity(vec_docs, updated_queries)
        vec_queries = sparse.csr_matrix(vec_queries)



    rf_sim = cosine_similarity(vec_docs, updated_queries)
    return rf_sim