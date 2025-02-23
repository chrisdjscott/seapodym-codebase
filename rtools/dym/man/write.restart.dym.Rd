% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/write_varDYM.R
\name{write.restart.dym}
\alias{write.restart.dym}
\title{Writes DYM file with population density initial conditions}
\usage{
write.restart.dym(file.out, x, y, mask, data)
}
\arguments{
\item{file.out}{is the name of the DYM file.}

\item{x}{is the vector of longitude.}

\item{y}{is the vector of latitude.}

\item{mask}{is the land mask - the matrix of integers 0 - 2, with 0 for land, 1 for the sea with only one layer (nearshore), 2 for the sea with two layers and 3 for the sea with three pelagic layers though the depth column.}

\item{data}{is the 3d array of data to be written in DYM file with the structure data[age,x,y]. The mean age of each age class is not written currently in this file, although it can be passed to zlevel. In the current version, zlevel is filled with age indices.}
}
\description{
Writes DYM file with population density initial conditions
}
\examples{
write.restart.dym("skj_cohorts.dym",x,y,mask,var);
}
