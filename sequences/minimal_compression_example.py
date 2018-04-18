from __future__ import division
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
import os
from information_entropy.utils import get_color_cycle, get_line_cycle, poly_fit, block_entropy, lempel_ziv_complexity
from information_entropy.compression import get_comp_size_bytes
from information_entropy.models.binary_sequences import (generate_checkerboard_seq,
                                                         generate_const_seq,
                                                         generate_fibonacci_seq,
                                                         generate_kolakoski_seq,
                                                         generate_random_seq,
                                                         generate_rudin_shapiro_seq,
                                                         generate_thue_morse_seq,
                                                         generate_pi_seq)

#######################SET LATEX OPTIONS###################
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
# rc('text.latex',preamble=r'\usepackage{times}')
glob_fontsize = 12
plt.rcParams.update({'font.size': glob_fontsize})
plt.rcParams['xtick.major.pad'] = 8
plt.rcParams['ytick.major.pad'] = 8
plt.rcParams.update({'figure.autolayout': True})


##########################################################


class SequenceResults(object):
    def __init__(self, sequence, get_sequence_output, n_list):
        self.seq = np.asarray(sequence, dtype='uint8')
        self.n_list = np.asarray(n_list)
        self.out = np.asarray(get_sequence_output)
        self.seq_size_list = self.out[:, 0]  # size of sequence after all iterations
        self.seq_nc_list = self.out[:, 1]  # number of compression
        self.seq_size1_list = self.out[:, 2]  # size of sequence after the first compression


def get_compressed_sequence(n_list, func, fname, algorithm='deflate', rle=False, blocksize=6):
    n_max = n_list[-1]
    sequence = None
    if os.path.isfile(fname):
        with open(fname, "rb") as ifile:
            sequence = pickle.load(ifile)
            seq = sequence.seq
    if sequence is not None and seq.size < n_max:
        assert np.array_equal(sequence.n_list, n_list[:len(sequence.n_list)])
        seq = func(n_max, seq)
        if 'block' in algorithm:
            out = np.array(
                [[block_entropy(seq[:n], blocksize), 1, 1] for n in n_list[sequence.n_list.size:]])
        elif 'lz76' in algorithm:
            out = np.array(
                [[lempel_ziv_complexity(seq[:n], version='lz76'), 1, 1] for n in n_list[sequence.n_list.size:]])
        elif 'lz77' in algorithm:
            f = lambda x: lempel_ziv_complexity(x, version='lz77')[0]
            out = np.array([[f(seq[:n]), 1, 1] for n in n_list[sequence.n_list.size:]])
        else:
            out = np.array(
                [get_comp_size_bytes(seq[:n], algorithm=algorithm, rle=rle) for n in n_list[sequence.n_list.size:]])
        print "new out ", out.shape
        print "existing out ", sequence.out.shape
        out = np.vstack((sequence.out, out))
        sequence = SequenceResults(seq, out, n_list)
        with open(fname, "wb") as ofile:
            pickle.dump(sequence, ofile, protocol=-1)
    elif sequence is not None and seq.size >= n_max:
        assert np.array_equal(sequence.n_list[:len(n_list)], n_list)
        out = sequence.out[:len(n_list), :]
    else:
        seq = func(n_max, np.empty(0, dtype='uint8'))
        if 'block' in algorithm:
            out = np.array([[block_entropy(seq[:n], blocksize), 1, 1] for n in n_list])
        elif 'lz76' in algorithm:
            out = np.array([[lempel_ziv_complexity(seq[:n], version='lz76'), 1, 1] for n in n_list])
        elif 'lz77' in algorithm:
            f = lambda x: lempel_ziv_complexity(x, version='lz77')[0]
            out = np.array([[f(seq[:n]), 1, 1] for n in n_list])
        else:
            out = np.array([get_comp_size_bytes(seq[:n], algorithm=algorithm, rle=rle) for n in n_list])

        sequence = SequenceResults(seq, out, n_list)
        with open(fname, "wb") as ofile:
            pickle.dump(sequence, ofile, protocol=-1)
    return out


if __name__ == "__main__":
    algorithm = 'block'
    Nmax = int(8) * 200
    n_list = np.arange(16, Nmax, 8) ** 2

    if True:
        # proc1 = Process(target=get_compressed_sequence, args=(n_list, generate_const_seq, "constant_sequence.pickle",))
        out = get_compressed_sequence(n_list, generate_const_seq, "constant_sequence_{}.pickle".format(algorithm),
                                      algorithm=algorithm)
        const_seq_size_list, const_seq_nc_list, const_seq_size1_list = out[:, 0], out[:, 1], out[:, 2]

        out = get_compressed_sequence(n_list, generate_checkerboard_seq,
                                      "checkerboard_sequence_{}.pickle".format(algorithm), algorithm=algorithm)
        check_seq_size_list, check_seq_nc_list, check_seq_size1_list = out[:, 0], out[:, 1], out[:, 2]

        out = get_compressed_sequence(n_list, generate_random_seq, "random_sequence_{}.pickle".format(algorithm),
                                      algorithm=algorithm)
        rand_seq_size_list, rand_seq_nc_list, rand_seq_size1_list = out[:, 0], out[:, 1], out[:, 2]

    if True:
        out = get_compressed_sequence(n_list, generate_rudin_shapiro_seq,
                                      "rudin_shapiro_sequence_{}.pickle".format(algorithm), algorithm=algorithm)
        rs_seq_size_list, rs_seq_nc_list, rs_seq_size1_list = out[:, 0], out[:, 1], out[:, 2]

        out = get_compressed_sequence(n_list, generate_thue_morse_seq,
                                      "thue_morse_sequence_{}.pickle".format(algorithm), algorithm=algorithm)
        tm_seq_size_list, tm_seq_nc_list, tm_seq_size1_list = out[:, 0], out[:, 1], out[:, 2]

        out = get_compressed_sequence(n_list, generate_fibonacci_seq, "fibonacci_sequence_{}.pickle".format(algorithm),
                                      algorithm=algorithm)
        fib_seq_size_list, fib_seq_nc_list, fib_seq_size1_list = out[:, 0], out[:, 1], out[:, 2]

    if False:
        out = get_compressed_sequence(n_list, generate_kolakoski_seq, "kolakoski_sequence_{}.pickle".format(algorithm),
                                      algorithm=algorithm)
        kol_seq_size_list, kol_seq_nc_list, kol_seq_size1_list = out[:, 0], out[:, 1], out[:, 2]

    fig0 = plt.figure()
    ax0 = fig0.add_subplot(111)
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    # ax0.plot(n_list ** 2, n_list ** 2, color='k', label='raw')
    ccycle = get_color_cycle(6)
    lcycle = get_line_cycle()


    def fit(x, y, p=10):
        fit_fn, fit_params, fit_err, rho = poly_fit(np.log(x)[-p:], np.log(y)[-p:])
        yfit = lambda xx: np.exp(fit_fn(np.log(xx)))
        return yfit, fit_params


    p = 110
    x = n_list

    if True:
        x, y = n_list, np.array(const_seq_size_list) / n_list
        color, linestyle = ccycle.next(), '-'
        ax0.plot(x, y, color=color, label='comp. constant', linewidth=2.5, linestyle=linestyle)
        yfit, fit_params = fit(x, y, p=p)
        ax0.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='constant {:.3f}'.format(fit_params[0]))
        ax1.plot(x, const_seq_nc_list, color=color, label='comp. constant', linewidth=5, linestyle=linestyle)
        x, y = const_seq_size1_list, const_seq_size_list / const_seq_size1_list
        ax2.plot(x, y, color=color, label='comp. constant', linewidth=2.5, linestyle=linestyle)
        # yfit, fit_params = fit(x, y, p=p)
        # ax2.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='constant {:.3f}'.format(fit_params[0]))

        x, y = n_list, np.array(check_seq_size_list) / n_list
        color, linestyle = ccycle.next(), '-'
        ax0.plot(x, y, color=color, label='comp. checkerboard', linewidth=2.5, linestyle=linestyle)
        yfit, fit_params = fit(x, y, p=p)
        ax0.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='checkerboard {:.3f}'.format(fit_params[0]))
        ax1.plot(x, check_seq_nc_list, color=color, label='comp. checkerboard', linewidth=2.5, linestyle=linestyle)
        x, y = check_seq_size1_list, check_seq_size_list / check_seq_size1_list
        ax2.plot(x, y, color=color, label='comp. checkerboard', linewidth=2.5, linestyle=linestyle)
        # yfit, fit_params = fit(x, y, p=p)
        # ax2.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='checkerboard {:.3f}'.format(fit_params[0]))

        x, y = n_list, np.array(rand_seq_size_list) / n_list
        color, linestyle = ccycle.next(), '-'
        ax0.plot(x, y, color=color, label='comp. random', linewidth=2.5, linestyle=linestyle)
        yfit, fit_params = fit(x, y, p=p)
        ax0.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='random {:.3f}'.format(fit_params[0]))
        ax1.plot(x, rand_seq_nc_list, color=color, label='comp. random', linewidth=2.5, linestyle=linestyle)
        x, y = rand_seq_size1_list, rand_seq_size_list / rand_seq_size1_list
        ax2.plot(x, y, color=color, label='comp. random', linewidth=2.5, linestyle=linestyle)
        # yfit, fit_params = fit(x, y, p=p)
        # ax2.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='random {:.3f}'.format(fit_params[0]))

    if True:
        x, y = n_list, np.array(rs_seq_size_list) / n_list
        color, linestyle = ccycle.next(), '-'
        ax0.plot(x, y, color=color, label='comp. rudin shapiro', linewidth=2.5, linestyle=linestyle)
        yfit, fit_params = fit(x, y, p=p)
        ax0.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='rudin shapiro {:.3f}'.format(fit_params[0]))
        ax1.plot(x, rs_seq_nc_list, color=color, label='comp. rudin shapiro', linewidth=2.5, linestyle=linestyle)
        x, y = rs_seq_size1_list, rs_seq_size_list / rs_seq_size1_list
        ax2.plot(x, y, color=color, label='comp. rudin shapiro', linewidth=2.5, linestyle=linestyle)
        # yfit, fit_params = fit(x, y, p=p)
        # ax2.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='rudin shapiro {:.3f}'.format(fit_params[0]))

        x, y = n_list, np.array(tm_seq_size_list) / n_list
        color, linestyle = ccycle.next(), '-'
        ax0.plot(x, y, color=color, label='comp. thue morse', linewidth=2.5, linestyle=linestyle)
        yfit, fit_params = fit(x, y, p=p)
        ax0.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='thue morse {:.3f}'.format(fit_params[0]))
        ax1.plot(x, tm_seq_nc_list, color=color, label='comp. thue morse', linewidth=2.5, linestyle=linestyle)
        x, y = tm_seq_size1_list, tm_seq_size_list / tm_seq_size1_list
        ax2.plot(x, y, color=color, label='comp. thue morse', linewidth=2.5, linestyle=linestyle)
        # yfit, fit_params = fit(x, y, p=p)
        # ax2.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='thue morse {:.3f}'.format(fit_params[0]))

        x, y = n_list, np.array(fib_seq_size_list) / n_list
        color, linestyle = ccycle.next(), '-'
        ax0.plot(x, y, color=color, label='comp. fibonacci', linewidth=2.5, linestyle=linestyle)
        yfit, fit_params = fit(x, y, p=p)
        ax0.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='fibonacci {:.3f}'.format(fit_params[0]))
        ax1.plot(x, fib_seq_nc_list, color=color, label='comp. fibonacci', linewidth=2.5, linestyle=linestyle)
        x, y = fib_seq_size1_list, fib_seq_size_list / fib_seq_size1_list
        ax2.plot(x, y, color=color, label='comp. fibonacci', linewidth=2.5, linestyle=linestyle)
        # yfit, fit_params = fit(x, y, p=p)
        # ax2.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='fibonacci {:.3f}'.format(fit_params[0]))

    if False:
        x, y = n_list, np.array(kol_seq_size_list) / n_list
        color, linestyle = ccycle.next(), '-'
        ax0.plot(x, y, color=color, label='comp. kolakoski', linewidth=2.5, linestyle=linestyle)
        yfit, fit_params = fit(x, y, p=p)
        ax0.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='kolakoski {:.3f}'.format(fit_params[0]))
        ax1.plot(x, kol_seq_nc_list, color=color, label='comp. kolakoski', linewidth=2.5, linestyle=linestyle)
        x, y = kol_seq_size1_list, kol_seq_size_list / kol_seq_size1_list
        ax2.plot(x, y, color=color, label='comp. kolakoski', linewidth=2.5, linestyle=linestyle)
        yfit, fit_params = fit(x, y, p=p)
        ax2.plot(x[-p:], yfit(x[-p:]), color='b', linestyle='--', label='kolakoski {:.3f}'.format(fit_params[0]))

    ax0.set_yscale('log')
    ax0.set_xscale('log')
    ax0.set_ylabel('bytes / raw bytes')
    ax0.set_xlabel('raw bytes')
    ax0.legend(loc='best')
    fig0.tight_layout()
    fig0.savefig('frac_comparison.png')

    ax1.set_xscale('log')
    ax1.set_ylabel(r'$n_c$')
    ax1.set_xlabel('raw bytes')
    ax1.legend(loc='best')
    fig1.tight_layout()
    fig1.savefig('ncompress_comparison.png')

    ax2.set_yscale('log')
    ax2.set_xscale('log')
    ax2.set_ylabel('bytes last compression / bytes first compression')
    ax2.set_xlabel('bytes first compression')
    ax2.legend(loc='best')
    fig2.tight_layout()
    fig2.savefig('compression_ratio_comparison.png')

    plt.show()