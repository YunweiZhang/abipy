#!/usr/bin/env python
from __future__ import division, print_function

import abipy.abilab as abilab
import abipy.data as data


def make_template():
    """Build a template input file for GS calculations with paral_kgb"""
    inp = abilab.AbiInput(pseudos=data.pseudos("14si.pspnc"))
    inp.set_structure(data.structure_from_ucell("Si"))

    # GS run with paral_kgb
    inp.set_kmesh(ngkpt=[8, 8, 8], shiftk=[0,0,0])

    # Global variables
    global_vars = dict(ecut=20,
                       nsppol=1,
                       nband=40,
                       paral_kgb=1,
                       npkpt=1,
                       npband=1,
                       npfft=1,
                       #
                       timopt=-1,
                       chksymbreak=0,
                       prtwf=0,
                       prtden=0,
                       tolvrs=1e-8,
                       nstep=10,
                    )
    inp.set_variables(**global_vars)

    return inp


def build_flow(mpi_ncpus=10):
    template = make_template()

    #policy = dict(autoparal=0, max_ncpus=mpi_ncpus)
    #manager = abilab.TaskManager.simple_mpi(mpi_ncpus=1, policy=policy)
    manager = abilab.TaskManager.from_user_config()
    manager.set_mpi_ncpus(mpi_ncpus)

    flow = abilab.AbinitFlow(workdir="gs_paral_kgb", manager=manager)

    for fftalg in [312, 402, 401]:
        work = abilab.Workflow()
        for inp in abilab.input_gen(template, fftalg=fftalg, ecut=range(10, 20, 5)):
            work.register(inp)
        flow.register_work(work)

    return flow.allocate()


def main():
    flow = build_flow()
    return flow.build_and_pickle_dump()


if __name__ == "__main__":
    import sys
    sys.exit(main())
