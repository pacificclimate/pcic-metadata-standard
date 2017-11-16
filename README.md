# PCIC Metadata Standard - Plugged In

Tool for managing the PCIC Metadata Standard.

## Rationale

The PCIC Metadata Standard (unfortunate acronym: PMS) establishes standards for metadata in the outputs of several
different tools, including GCM output downscaling (BCCAQ et al.), gridded observations, hydrological modelling (VIC), 
and routed streamflow modelling (RVIC). From any of these datasets, we form CLIMDEX indices, climatological means,
and other derived products.

Data flows in roughly the sequence named above; namely, from observations or GCM outputs through hydrological modelling
and thence through streamflow modelling, with derived products from each. 
The metadata in the output from each stage of processing must contain sufficient information to identify or at least
characterize both itself and the its key data inputs.

Because there is a lot of repetition (metadata flowing from previous stages to later stages), 
the metadata standards for each type of output file 
share many metadata attributes with the others (with a disciplined naming schema to ensure that no confusion results).
This makes manual maintenance painful and error prone. This is a job for computers.

## Design

Metadata attributes are collected together into _groups_ of related attributes. 
For example, there is the _PCIC CMIP5 Common Subset_,
which is a standard subset of the CMIP5 metadata attributes that PCIC has adopted for inclusion in all its output
data files. Another example is the __, which identifies an external dataset that is used to 
calibrate or force a model.

Metadata attribute groups are divided into two types: _atomic_ and _composite_.

An atomic group is a collection of metadata attributes. (Each attribute has a name, description, 
required (mandatory/optional) flag, and other information.)

A composite group is a collection of groups, either atomic or composite. 
Each group in the collection is associated with an optional _attribute name prefix_ (just prefix for short)
that enables us to generate unambigous names within the containing group as a whole, 
and with a _role_ that is a brief string that describes the relationship of the
contained group to the whole.

