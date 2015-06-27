from __future__ import division
import numpy as np
import h5py

f_h5 = "db/JJ_noun_phrase.h5"
h5   = h5py.File(f_h5, 'r')

def anti_word(source_idx,source,target,cutoff=-.002):
    '''
    Returns a distance and word that is far from the target 
    from an SVD approximation.
    '''
    
    distance = np.dot(target, (source*var)[source_idx])
    distance /= np.linalg.norm(distance)

    cut_idx  = distance<cutoff
    
    idx = np.arange(*distance.shape,dtype=int)[cut_idx]
    keep_idx = np.random.choice(idx)

    return distance, keep_idx

def absurd_JJ_JJ_NN(noun_idx=None, cutoff=-0.002):

    if noun_idx == None:
        noun_idx = np.random.randint(vocab_nouns.size)

    noun_dist, adj_idx1 = anti_word(noun_idx,
                            source=svd_nouns,
                            target=svd_adjs,
                            cutoff=cutoff)

    adj_dist, adj_idx2 = anti_word(adj_idx1,
                                   source=svd_adjs,
                                   target=svd_adjs,
                                   cutoff=cutoff)

    noun = vocab_nouns[noun_idx]
    adj1 = vocab_adjs[adj_idx1]
    adj2 = vocab_adjs[adj_idx2]

    scores = noun_dist[adj_idx1], noun_dist[adj_idx2], adj_dist[adj_idx2]
    return (adj1,adj2,noun), scores


def quality_filter(noun=None, low=-0.075, high=-0.010):
    '''
    Generates absurd phrases that are not too absurd (which are boring,
    they use common adjectives), yet still have that je nes se pas
    '''
    total_score = 0
    while not low < total_score < high:
        phrase, scores = absurd_JJ_JJ_NN(noun, cutoff=cutoff)
        total_score = sum(scores)
    return phrase, scores

if __name__ == "__main__":
    verbose = True

    eigenvalue_cut = 300
    common_nouns   = 200
    common_adjs    = 400

    vocab_nouns = h5["nouns"]["words"][common_nouns:]
    vocab_adjs  = h5["adjs"]["words"][common_adjs:]

    svd_nouns = h5["nouns"]["svd"][common_nouns:,:eigenvalue_cut]
    svd_adjs = h5["nouns"]["svd"][common_adjs:,:eigenvalue_cut]
    var = h5["variance"][:eigenvalue_cut]

    explained_variance = var[:,0].sum()

    # So we can multiply them together
    var = var.reshape(-1)

    print "Explained variance in sample: ", explained_variance
    cutoff = -.005

    for k in xrange(500):
        phrase, scores = quality_filter()

        if verbose:
            s1,s2,s3 = scores
            output = "{: 0.3f} {: 0.3f} {: 0.3f} {: 0.3f} {:20s}"
            output_vals = sum(scores),s1,s2,s3, ' '.join(phrase)
        else:
            output = "{:.4f} {:20s}"
            output_vals = sum(scores), ' '.join(phrase)

        print output.format(*output_vals)
