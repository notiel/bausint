from typing import Tuple, List
import math

L_dict = {'L1': 5939.58, 'L2': 6287.40, 'L5': 6338.55}

L1_regs = [0x00302510,
           0x0F53f7C1,
           0x01D007D2,
           0x00000003,
           0x32008984,
           0x00800025,
           0x35008476,
           0x060000E7,
           0x15596568,
           0x07047CC9,
           0x00C0067A,
           0x0061200B,
           0x000015FC,
           0x0000000D]

L2_regs = [0x00302740,
           0x0BD70A31,
           0x00540192,
           0x00000003,
           0x32008984,
           0x00800025,
           0x35008476,
           0x060000E7,
           0x15596568,
           0x07047CC9,
           0x00C0067A,
           0x0061200B,
           0x000015FC,
           0x0000000D]

L5_regs = [0x00302790,
           0x0DAE1471,
           0x00440192,
           0x00000003,
           0x32008984,
           0x00800025,
           0x35008476,
           0x060000E7,
           0x15596568,
           0x07047CC9,
           0x00C0067A,
           0x0061200B,
           0x000015FC,
           0x0000000D]

L_reg_dict = {'L1': L1_regs, 'L2': L2_regs, 'L5':L5_regs}


def get_regs(move: int, state: str) -> Tuple[int, int, int, int]:
    """
    get registers move for
    :param move:
    :param state:
    :return:
    """
    step: int = 500
    freq_d: int = 10
    freq: float = L_dict[state]
    freq_ratio: float = (freq + (move / 1000000)) / freq_d

    freq_ration_int: int = int(freq_ratio)
    reg_value: int = 0x000000
    reg0: int = (freq_ration_int << 4) | 0x300000 | reg_value

    remain1: float = freq_ratio - freq_ration_int
    frac: float = remain1 * 2**24
    frac1: int = int(frac)
    reg_value: int = 0x000001
    reg1: int = frac1 << 4 | reg_value

    remain2: int = round(frac - frac1, 5)
    mod2: int = (10**7)//step
    frac2: int = int(remain2 * mod2)
    nod: int = math.gcd(frac2, mod2)
    frac2 //= nod
    mod2 //= nod
    lsb_frac: int = frac2 & 0b00000000000000000011111111111111
    lsb_mod: int = mod2 & 0b00000000000000000011111111111111
    reg_value: int = 0x000002
    reg2: int = ((lsb_frac << 18) | lsb_mod << 4) | reg_value

    msb_fraq: int = frac2 & 0b00001111111111111100000000000000
    msb_mod: int = mod2 & 0b00001111111111111100000000000000
    reg_value: int = 0x00000D
    reg_d: int = ((msb_fraq << 4) | (msb_mod >> 10)) | reg_value
    return reg0, reg1, reg2, reg_d


def get_reg_str(state: str, move: int) -> str:
    """
    gets registers string to send to pcb
    :param move: shift of frequency in Hz
    :param state:l1, l2 or l5
    :return:
    """
    if not state:
        state = 'L1'
    old_regs: List[str] = L_reg_dict[state]
    new_regs: List[str] = old_regs.copy()
    if move:
        new_regs[0], new_regs[1], new_regs[2], new_regs[13] = get_regs(move, 'L1')
    regs_str: List[str] = ['0x%08x' % int(reg) for reg in new_regs]
    # regs_str = [str(reg) for reg in new_regs]
    res: str = ' '.join(regs_str)
    return res
