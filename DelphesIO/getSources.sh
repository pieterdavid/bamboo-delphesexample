#!/bin/sh
if [ $# != 1 ]; then
  echo "One argument, the Delphes version, is required"
  exit 1
fi
delphestag="${1}"
wget -q -P include "https://raw.githubusercontent.com/delphes/delphes/${delphestag}/classes/DelphesClasses.h"
wget -q -P include "https://raw.githubusercontent.com/delphes/delphes/${delphestag}/classes/DelphesFactory.h"
wget -q -P include "https://raw.githubusercontent.com/delphes/delphes/${delphestag}/classes/SortableObject.h"
wget -q -P src "https://raw.githubusercontent.com/delphes/delphes/${delphestag}/classes/DelphesClasses.cc"
wget -q -P src "https://raw.githubusercontent.com/delphes/delphes/${delphestag}/classes/DelphesFactory.cc"
wget -q -P src "https://raw.githubusercontent.com/delphes/delphes/${delphestag}/external/ExRootAnalysis/ExRootTreeBranch.h"
wget -q -P src "https://raw.githubusercontent.com/delphes/delphes/${delphestag}/external/ExRootAnalysis/ExRootTreeBranch.cc"
wget -q -P src "https://raw.githubusercontent.com/delphes/delphes/${delphestag}/classes/ClassesLinkDef.h"
patch -p1 -i $(dirname $0)/sources.patch
