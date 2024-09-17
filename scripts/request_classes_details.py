
import inspect

class Table():
   pass

## AUTO
class CfStandardName(Table):
    """CF Standard Names (copied into data request to facilitate validation, particularly validation of consistency of definition in the CF standard with usage in the data request)."""

## END
    def __init__(self):
        pass


## AUTO
class CellMeasures(Table):
    """This can be either a string value for inclusion in the NetCDF variable attribute cell_measures, or a directive. In the latter case it will be a single word, --OPT or --MODEL. The first of these indicates that the data may be provided either on the cell centres or on the cell boundaries. --MODEL indicates that the data should be provided at the cell locations used for that variable in the model code (e.g. cell vertices)."""

## END
    def __init__(self):
        pass


## AUTO
class CellMethods(Table):
    """Description of cell methods entries"""

## END
    def __init__(self):
        pass


## AUTO
class CoordinateOrDimension(Table):
    """Dimensions used by variables in the data request"""

## END
    def __init__(self):
        pass


## AUTO
class DocsForOpportunities(Table):
    """Reference documents"""

## END
    def __init__(self):
        pass


## AUTO
class Experiment(Table):
    """The list of experiments is currently limited to those in the AR7 Fast Track, but there will be chance to propose new experiments for inclusion in the data request during Phase 2 of the consultation (October/November 2024)."""

## END
    def __init__(self):
        pass


## AUTO
class ExperimentGroup(Table):
    """These are non-exclusive grouping of experiments (e.g. ‘AR7 Fast Track’, ‘DECK’, ‘Scenarios’ etc.). Experiments can belong to more than one group. The list of experiments is currently limited to those in the Fast Track, but there will be chance to propose new experiments for inclusion in the data request during Phase 2 of the consultation (October/November 2024)."""

## END
    def __init__(self):
        pass


## AUTO
class Mip(Table):
    """Model Intercomparison Project"""

## END
    def __init__(self):
        pass


## AUTO
class Opportunity(Table):
    """These are the intended use-case/justification for one or multiple variable groups. Opportunities are linked to relevant experiment groups. Identifying opportunities helps to provide a structure to map variables against requirements. Each opportunity description will convey why this combination of variables and experiments is important and how they contribute to impact. 

"""

## END
    def __init__(self):
        pass


## AUTO
class PhysicalParameter(Table):
    """Each Physical Parameter record defines a MIP variable name, associated with a CF Standard Name.

Formerly known as MIP Variables in CMIP6"""

## END
    def __init__(self):
        pass


## AUTO
class SpatialShape(Table):
    """The spatial shape record contains the spatial dimensions of the field, and also, for convenience, an integer specifying the number of levels if that number is specified. A boolean level flag is set to “true” if the number of vertical levels is specified."""

## END
    def __init__(self):
        pass


## AUTO
class Structure(Table):
    """The structure record combines specification of dimensions, cell_measures and cell_methods attributes. Spatial and temporal dimensions are specified through links to “spatialshape” and “temporalshape” records."""

## END
    def __init__(self):
        pass


## AUTO
class TemporalShape(Table):
    """The temporal shape record contains the temporal dimensions."""

## END
    def __init__(self):
        pass


## AUTO
class TimeSlice(Table):
    """"""

## END
    def __init__(self):
        pass


## AUTO
class Variable(Table):
    """Each Output variable record corresponds to a MIP table variable specification. """

## END
    def __init__(self):
        pass


## AUTO
class VariableGroup(Table):
    """These are non-exclusive grouping of CMIP variables (e.g. monthly time slices of the baseline variables). Variables can belong to more than one group."""

## END
    def __init__(self):
        pass


tables = {x:v for x,v in locals().items() if x[0] != '_' and inspect.isclass(v) and issubclass(v , Table )}
print ( locals().keys() )
