# On the Subloading Surface Model for Metals: Some Insights and an Efficient Numerical Implementation

This repository contains the source code and example models of paper [10.1007/s00707-025-04339-0](https://doi.org/10.1007/s00707-025-04339-0).

To cite or reproduce figures in the paper, you can find the corresponding figure and copy the source code in your work.
Please check CI/CD workflow to see how to generate figures used in the paper.

The numerical examples used in the paper are developed in `suanPan`.
To perform the numerical analysis, one can download and install [`suanPan`](https://github.com/TLCFEM/suanPan).
Then run the model via, for example, the following command in the corresponding folders.

```sh
cd ./PIC/CYCLIC
suanpan -f cyclic.sp
```
