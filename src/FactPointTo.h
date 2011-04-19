// -*- mode: C++ -*-
//
// Copyright (c) 2007, 2008, 2009, 2010, 2011 The University of Utah
// All rights reserved.
//
// This file is part of `csmith', a random generator of C programs.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//   * Redistributions of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//
//   * Redistributions in binary form must reproduce the above copyright
//     notice, this list of conditions and the following disclaimer in the
//     documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

#ifndef FactPointTo_H
#define FactPointTo_H

///////////////////////////////////////////////////////////////////////////////

#include <ostream>
#include <vector>
#include "Fact.h"
 
class Variable;
class Function;
class Statement;
class Block;
class StatementAssign;
class StatementReturn;

using namespace std;

///////////////////////////////////////////////////////////////////////////////

class FactPointTo : public Fact
{
public:
 	static FactPointTo *make_fact(const Variable* v);  
	static FactPointTo *make_fact(const Variable* v, const vector<const Variable*>& set);
	static FactPointTo *make_fact(const Variable* v, const Variable* point_to);
	static vector<const Fact*> make_facts(vector<const Variable*> vars, const vector<const Variable*>& set);
	static vector<const Fact*> make_facts(vector<const Variable*> vars, const Variable* point_to);
	static void doFinalization();

	explicit FactPointTo(const Variable* v);
	virtual ~FactPointTo(void); 

	virtual const Variable* get_var(void) const { return var;};
	const vector<const Variable*>& get_point_to_vars(void) const { return point_to_vars; };

	bool is_null(void) const;
	bool is_tbd_only(void) const;
	bool is_dead(void) const;
	bool has_invisible(const Function* func, const Statement* stm) const;
	int  size() const;
	virtual std::vector<const Fact*> abstract_fact_for_assign(const std::vector<const Fact*>& facts, const Lhs* lhs, const Expression* rhs);
	virtual Fact* abstract_fact_for_return(const std::vector<const Fact*>& facts, const ExpressionVariable* var, const Function* func);

	FactPointTo* mark_dead_var(const Variable* v);
	FactPointTo* mark_func_end(const Statement* stm);
	const FactPointTo* update_with_modified_index(const Variable* index_var) const;

	virtual int join(const Fact& fact);  
	virtual int join_visits(const Fact& fact); 
	virtual Fact* clone(void) const;
	virtual bool conflict_with(const Fact& fact) const;
	virtual bool is_related(const Fact& fact) const;
	virtual bool is_relevant(const Fact& f) const;
	virtual bool equal(const Fact& fact) const;
	virtual void Output(std::ostream &out) const;

	virtual void OutputAssertion(std::ostream &out) const;
    
	static std::vector<const Variable*> merge_pointees_of_pointer(const Variable* ptr, int indirect, const std::vector<const Fact*>& facts);
	static std::vector<const Variable*> merge_pointees_of_pointers(const std::vector<const Variable*>& ptrs, const std::vector<const Fact*>& facts);
	static void update_facts_with_modified_index(std::vector<const Fact*>& facts, const Variable* var);
	static void aggregate_all_pointto_sets(void);

	static bool is_valid_ptr(const Variable* p, const std::vector<const Fact*>& facts);
	static bool is_valid_ptr(const char* name, const std::vector<const Fact*>& facts);
	static bool is_dangling_ptr(const Variable* p, const std::vector<const Fact*>& facts); 
	static bool is_dangling_expr(const Expression* e, const std::vector<const Fact*>& facts);
	static bool is_special_ptr(const Variable* p) { return p==null_ptr || p==garbage_ptr || p==tbd_ptr;}
	static bool is_pointing_to_locals(const Variable* v, const Block* b, int indirection, const vector<const Fact*>& facts); 

	static std::string point_to_str(const Variable* v);

	static const Variable* null_ptr;
	static const Variable* garbage_ptr;
	static const Variable* tbd_ptr;
	
	static vector<const Variable*> all_ptrs;
	static vector<vector<const Variable*> > all_aliases;
private:  
	FactPointTo(const Variable* v, const vector<const Variable*>& set);
	FactPointTo(const Variable* v, const Variable* point_to);

	const Variable* var;
	vector<const Variable*> point_to_vars; 
	static std::vector<FactPointTo*> facts_;
	
	static void update_ptr_aliases(const vector<Fact*>& facts, vector<const Variable*>& ptrs, vector<vector<const Variable*> >& aliases);

	// unimplement 
	FactPointTo(const FactPointTo& f);
	FactPointTo &operator=(const FactPointTo &ev);
};

///////////////////////////////////////////////////////////////////////////////

#endif // FactPointTo_H

// Local Variables:
// c-basic-offset: 4
// tab-width: 4
// End:

// End of file.