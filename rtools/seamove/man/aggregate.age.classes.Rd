% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/rw-seamove.R
\name{aggregate.age.classes}
\alias{aggregate.age.classes}
\title{Aggregating the age structure of the SEAPODYM movement fluxes to a coarser age structure used in the Multifan-CL model configuration.}
\usage{
\method{aggregate}{age.classes}(dir.in, dir.out, a0, am, a.plus = TRUE, aggregate.by = 3)
}
\arguments{
\item{dir.in}{is the SEAPODYM output directory containing files [spname]_FluxesRegion_age[a].txt, where a is the age class indices from 0 to A+.}

\item{dir.out}{is the new output directory containing files [spname]_FluxesRegion_age[a].txt with the age structure as defined in Multifan-CL.}

\item{a0, }{am are the first and last index of age classes to be extracted from the outputs in dir.in and aggregated to coarser age structure. The vector given by a0:am should be a sub-set of age classes in the outputs.}

\item{a.plus}{has the logical value, indicating whether the last age class in age.in is the A+. If yes, it will be used as is in the aggregation to Multifan-CL structure. Otherwise, it will be included in the aggregation.}

\item{aggregate.by}{is the size of the Multifan-CL age class in SEAPODYM age class units. Note, the Multifan-CL age indices start with 1 and not 0 as original SEAPODYM files.}
}
\value{
Returns the number of aggregated age classes.
}
\description{
Aggregating the age structure of the SEAPODYM movement fluxes to a coarser age structure used in the Multifan-CL model configuration.
}
\examples{
# Example of skipjack configuration with 49 age classes, aggregating
# classes older than 3 months of age, i.e., skipping the first three 
# monthly classes:
dir.in<-"SKJ-DIR/output"
dir.out<-"SKJ-DIR/output-mfcl/"
nba<-aggregate.age.classes(dir.in,dir.out,a0,am=48,age.plus=TRUE,aggregate.by=3)
}
