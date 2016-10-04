#!/bin/csh

foreach i ( [A-Z]*.in )

    echo Starting $i

    prover9 -f cs.in $i > $i:r-cs.outu

end
