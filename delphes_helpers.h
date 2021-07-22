#pragma once

#include <TObjArray.h>
#include <ROOT/RVec.hxx>

namespace rdfhelpers {
  template<typename OBJ>
  ROOT::VecOps::RVec<OBJ*> objArrayToRVec(const TObjArray& arr) {
    ROOT::VecOps::RVec<OBJ*> out{reinterpret_cast<OBJ**>(arr.GetObjectRef()), static_cast<std::size_t>(arr.GetEntries())};
    auto it = *dynamic_cast<TObjArrayIter*>(arr.MakeIterator());
    std::size_t i = 0;
    while ( ( i != out.size() ) && ( out[i] == *it ) ) {
      it.Next();
      ++i;
    }
    if ( i != out.size() ) { // not equal to contiguous array, copy pointers
      it.Reset();
      const auto n = out.size();
      out = ROOT::VecOps::RVec<OBJ*>();
      out.reserve(n);
      do {
        out.push_back(static_cast<OBJ*>(*it));
      } while ( it.Next() );
    }
    return out;
  }
};
