# This file includes Lua snippets

#checks needed: 721
MATHS = """
 function __mat_mul__(a, b)
    local a_rows, a_cols = #a, #a[0]
    local b_rows, b_cols = #b, #b[0]
    assert(a_cols == b_rows, "incompatible matrix sizes")

    local res = list()
    for i = 1, a_rows do
        res[i-1] = list()
        for j = 1, b_cols do
            res[i-1][j-1] = 0
            for k = 1, a_cols do
                res[i-1][j-1] += a[i-1][k-1] * b[k-1][j-1]
            end
        end
    end

    return res
end
"""

COMPLEX = """
local _cmplxMeta = {
	__index = function(n, index)
		if index == "real" then
			return n[1] 
		elseif index == "imag" then
			return n[2] 
		elseif index == "conjugate" then
			return function() return setmetatable({n[1], -n[2]}, getmetatable(n)) end
		end
	end,
	__newindex = function(n, index, value)
		if type(index) == "number" or type(index) == "string" then
			error(index .. " cannot be assigned to")
		else
			error("invalid argument #2 (number or string expected, got " .. typeof(index) .. ")")
		end
	end,
	__unm = function(n) -- Negates the number.
		return setmetatable({-n[1], -n[2]}, getmetatable(n))
	end,
	__add = function(n1, n2) -- Adds two numbers.
		if (type(n1) == "number" or type(n2) == "number") or (type(n1) == "table" and type(n2) == "table" and getmetatable(n1) == getmetatable(n2)) then
			if type(n1) == "number" then
				n1 = {n1, 0}
			end
			if type(n2) == "number" then
				n2 = {n2, 0}
			end

			local t1, t2
			if math.abs(n1[1]) == math.huge and math.abs(n2[1]) == math.huge and -n1[1] == n2 then
				t1 = 0
			else
				t1 = n1[1] + n2[1]
			end
			if math.abs(n1[2]) == math.huge and math.abs(n2[2]) == math.huge and -n1[2] == n2 then
				t2 = 0
			else
				t2 = n1[2] + n2[2]
			end

			return setmetatable({t1, t2}, getmetatable(n1) or getmetatable(n2))
		else
			if type(n1) == type(n2) then
				error("attempt to perform arithmetic (add) on " .. typeof(n1))
			else
				error("attempt to perform arithmetic (add) on " .. typeof(n1) .. "and" .. typeof(n2))
			end
		end
	end,
	__sub = function(n1, n2) -- Subtracts the first number with the second one.
		if (type(n1) == "number" or type(n2) == "number") or (type(n1) == "table" and type(n2) == "table" and getmetatable(n1) == getmetatable(n2)) then
			if type(n1) == "number" then
				n1 = {n1, 0}
			end
			if type(n2) == "number" then
				n2 = {n2, 0}
			end

			local t1, t2
			if math.abs(n1[1]) == math.huge and math.abs(n2[1]) == math.huge and n1[1] == n2[1] then
				t1 = 0
			else
				t1 = n1[1] - n2[1]
			end
			if math.abs(n1[2]) == math.huge and math.abs(n2[2]) == math.huge and n1[2] == n2[2] then
				t2 = 0
			else
				t2 = n1[2] - n2[2]
			end

			return setmetatable({t1, t2}, getmetatable(n1) or getmetatable(n2))
		else
			if type(n1) == type(n2) then
				error("attempt to perform arithmetic (sub) on " .. typeof(n1))
			else
				error("attempt to perform arithmetic (sub) on " .. typeof(n1) .. "and" .. typeof(n2))
			end
		end
	end,
	__mul = function(n1, n2) -- Multiply two numbers.
		if (type(n1) == "number" or type(n2) == "number") or (type(n1) == "table" and type(n2) == "table" and getmetatable(n1) == getmetatable(n2)) then
			if type(n1) == "number" then
				n1 = {n1, 0}
			end
			if type(n2) == "number" then
				n2 = {n2, 0}
			end

			local t1, t2 = n1[1] * n2[1] - n1[2] * n2[2], n1[1] * n2[2] + n2[1] * n1[2]
			if string.find(tostring(t1), "nan") and not string.find(tostring(n1[1]), "nan") and not string.find(tostring(n1[2]), "nan") and not string.find(tostring(n2[1]), "nan") and not string.find(tostring(n2[2]), "nan") then
				t1 = 0
			end
			if string.find(tostring(t2), "nan") and not string.find(tostring(n1[1]), "nan") and not string.find(tostring(n1[2]), "nan") and not string.find(tostring(n2[1]), "nan") and not string.find(tostring(n2[2]), "nan") then
				t2 = 0
			end

			return setmetatable({t1, t2}, getmetatable(n1) or getmetatable(n2))
		else
			if type(n1) == type(n2) then
				error("attempt to perform arithmetic (mul) on " .. typeof(n1))
			else
				error("attempt to perform arithmetic (mul) on " .. typeof(n1) .. "and" .. typeof(n2))
			end
		end
	end,
	__div = function(n1, n2) -- Divides two numbers.
		if (type(n1) == "number" or type(n2) == "number") or (type(n1) == "table" and type(n2) == "table" and getmetatable(n1) == getmetatable(n2)) then
			if type(n1) == "number" then
				n1 = {n1, 0}
			end
			if type(n2) == "number" then
				n2 = {n2, 0}
			end

			local t1, t2
			if (n1[1] == 0 and n1[2] == 0 and n2[1] == 0 and n2[2] == 0) or ((math.abs(n1[1]) == math.huge or math.abs(n1[2]) == math.huge) and (math.abs(n2[1]) == math.huge or math.abs(n2[2]) == math.huge)) then
				t1, t2 = tonumber("-nan(ind)"), tonumber("-nan(ind)")
			elseif math.abs(n1[1]) == math.huge or math.abs(n1[2]) == math.huge then
				t1 = (setmetatable({n1[1], 0}, getmetatable(n1) or getmetatable(n2)) * setmetatable({n2[1], 0}, getmetatable(n1) or getmetatable(n2)) + setmetatable({n1[2], 0}, getmetatable(n1) or getmetatable(n2)) * setmetatable({n2[2], 0}, getmetatable(n1) or getmetatable(n2)))[1] / (n2[1] ^ 2 + n2[2] ^ 2)
				t2 = (setmetatable({n1[2], 0}, getmetatable(n1) or getmetatable(n2)) * setmetatable({n2[1], 0}, getmetatable(n1) or getmetatable(n2)) - setmetatable({n1[1], 0}, getmetatable(n1) or getmetatable(n2)) * setmetatable({n2[2], 0}, getmetatable(n1) or getmetatable(n2)))[1] / (n2[1] ^ 2 + n2[2] ^ 2)
			elseif math.abs(n2[1]) == math.huge or math.abs(n2[2]) == math.huge then
				t1, t2 = 0, 0
			else
				t1 = (n1[1] * n2[1] + n1[2] * n2[2]) / (n2[1] ^ 2 + n2[2] ^ 2)
				t2 = (n1[2] * n2[1] - n1[1] * n2[2]) / (n2[1] ^ 2 + n2[2] ^ 2)
			end

			if tostring(t1) == "nan" and (tostring(n1[1]) ~= "nan" or tostring(n2[1]) ~= "nan") then
				t1 = 0
			end
			if tostring(t2) == "nan" and (tostring(n1[2]) ~= "nan" or tostring(n2[2]) ~= "nan") then
				t2 = 0
			end

			return setmetatable({t1, t2}, getmetatable(n1) or getmetatable(n2))
		else
			if type(n1) == type(n2) then
				error("attempt to perform arithmetic (div) on " .. typeof(n1))
			else
				error("attempt to perform arithmetic (div) on " .. typeof(n1) .. "and" .. typeof(n2))
			end
		end
	end,
	__pow = function(n1, n2)
		local function __asin(x)
			return 1 / math.sin(x)
		end

		local function __acos(x)
			return 1 / math.cos(x)
		end

		local function __atan(x)
			return 1 / math.tan(x)
		end

		if (type(n1) == "number" or type(n2) == "number") or (type(n1) == "table" and type(n2) == "table" and getmetatable(n1) == getmetatable(n2)) then
			if type(n1) == "number" then
				n1 = {n1, 0}
			end
			if type(n2) == "number" then
				n2 = {n2, 0}
			end

			local z, ex, i
			local norm = math.sqrt(n1[1] ^ 2 + n1[2] ^ 2)
			if norm ~= 0 then
				z = setmetatable({math.log(norm), math.atan2(n1[2], n1[1])}, getmetatable(n1))
				ex = n2 * z
				norm = math.exp(ex[1])
				i = ex[2]
			else
				norm = 0
				i = 0
			end

			return setmetatable({norm * math.cos(i), norm * math.sin(i)}, getmetatable(n1) or getmetatable(n2))
		else
			if type(n1) == type(n2) then
				error("attempt to perform arithmetic (pow) on " .. typeof(n1))
			else
				error("attempt to perform arithmetic (pow) on " .. typeof(n1) .. "and" .. typeof(n2))
			end
		end
	end,
	__eq = function(n1, n2) -- Tests for equality.
		if (type(n1) == "number" or type(n2) == "number") or (type(n1) == "table" and type(n2) == "table" and getmetatable(n1) == getmetatable(n2)) then
			if type(n1) == "number" then
				n1 = {n1, 0}
			end
			if type(n2) == "number" then
				n2 = {n2, 0}
			end

			return (n1[1] == n2[1]) and (n1[2] == n2[2])
		else
			return false
		end
	end,
	__tostring = function(n) -- Converts CmplxNumber datatype to a string.
		local t1, t2
		if n[1] == 0 and n[2] == 0 then
			t1 = "0"
		elseif n[1] == 0 then
			t1 = ""
		else
			t1 = tostring(n[1])
		end
		if n[2] == 0 then
			t2 = ""
		elseif n[2] == 1 then
			if n[1] == 0 then
				t2 = "i"
			else
				t2 = "+i"
			end	
		elseif n[2] == -1 then
			t2 = "-i"
		else
			if string.find(tostring(n[2]), "e") or string.find(tostring(n[2]), "inf") or string.find(n[2], "nan") then
				t2 = tostring(n[2]) .. "*i"
			else
				t2 = tostring(n[2]) .. "i"
			end
			if n[1] ~= 0 and string.sub(tostring(n[2]), 1, 1) ~= "-" then
				t2 = "+" .. t2
			end
		end

		return t1 .. t2
	end,
	__type = function(n)
		return typeof(n)
	end,
}

local _cmplxFactory = {
	__call = function(t, re, im)
		re = type(re) == "number" and re or 0
		im = type(im) == "number" and im or 0
		local cmplx = { re, im }
		setmetatable(cmplx, _cmplxMeta)
		return cmplx
	end
}

complex = setmetatable({}, _cmplxFactory)
"""

struct = """
local struct = {}

function struct.pack(format: string, size: number?, ...)
	local predictedSize = size or 2048
	local vars = {...}

	local stream = buffer.create(predictedSize)
	local endianness = true

	local ind = 0

	for i = 1, format:len() do
		local opt = (format:sub(i, i) :: string)

		if opt == '<' then
			endianness = true
		elseif opt == '>' then
			endianness = false
		elseif opt:find('[bBhHiIlL]') then
			local n = opt:find('[hH]') and 2 or opt:find('[iI]') and 4 or opt:find('[lL]') and 8 or 1
			local val = (tonumber(table.remove(vars, 1)) :: number)

			local bytes = {}
			for j = 1, n do
				table.insert(bytes, string.char(val % (2 ^ 8)))
				val = math.floor(val / (2 ^ 8))
			end
			local data
			if not endianness then
				data = string.reverse(table.concat(bytes))
			else
				data = table.concat(bytes)
			end
			buffer.writestring(stream, ind, data)
			ind += #data
		elseif opt:find('[fd]') then
			local val = (tonumber(table.remove(vars, 1))  :: number)
			local sign = 0

			if val < 0 then
				sign = 1
				val = (-val :: number)
			end

			local mantissa, exponent = math.frexp(val)
			if val == 0 then
				mantissa = 0
				exponent = 0
			else
				mantissa = (mantissa * 2 - 1) * math.ldexp(0.5, (opt == 'd') and 53 or 24)
				exponent = exponent + ((opt == 'd') and 1022 or 126)
			end

			local bytes = {}
			if opt == 'd' then
				val = mantissa
				for i = 1, 6 do
					table.insert(bytes, string.char(math.floor(val) % (2 ^ 8)))
					val = math.floor(val / (2 ^ 8))
				end
			else
				table.insert(bytes, string.char(math.floor(mantissa) % (2 ^ 8)))
				val = math.floor(mantissa / (2 ^ 8))
				table.insert(bytes, string.char(math.floor(val) % (2 ^ 8)))
				val = math.floor(val / (2 ^ 8))
			end

			table.insert(bytes, string.char(math.floor(exponent * ((opt == 'd') and 16 or 128) + val) % (2 ^ 8)))
			val = math.floor((exponent * ((opt == 'd') and 16 or 128) + val) / (2 ^ 8))
			table.insert(bytes, string.char(math.floor(sign * 128 + val) % (2 ^ 8)))
			val = math.floor((sign * 128 + val) / (2 ^ 8))

			local data
			if not endianness then
				data = string.reverse(table.concat(bytes))
			else
				data = table.concat(bytes)
			end
			buffer.writestring(stream, ind, data)
			ind += #data
		elseif opt == 's' then
			local data = tostring(table.remove(vars, 1))

			buffer.writestring(stream, ind, data)
			ind += #data
			buffer.writestring(stream, ind, string.char(0))
			ind += 1
		elseif opt == 'c' then
			local n = format:sub(i + 1):match('%d+')
			local str = tostring(table.remove(vars, 1))
			local len = (tonumber(n) :: number)
			if len <= 0 then
				len = str:len()
			end
			if len - str:len() > 0 then
				str = str .. string.rep(' ', len - str:len())
			end
			local data = str:sub(1, len)
			buffer.writestring(stream, ind, data)
			ind += #data
			i = i + (n :: string):len()
		end
	end

	return buffer.tostring(stream)
end

function struct.unpack(format: string, stream: string, pos: number?)
        local stream = buffer.fromstring(stream)
	local vars = {}
	local iterator = pos or 1
	local endianness = true

	for i = 1, format:len() do
		local opt: string = format:sub(i, i)

		if opt == '<' then
			endianness = true
		elseif opt == '>' then
			endianness = false
		elseif opt:find('[bBhHiIlL]') then
			local n = opt:find('[hH]') and 2 or opt:find('[iI]') and 4 or opt:find('[lL]') and 8 or 1
			local signed = opt:lower() == opt

			local val = 0
			for j = 1, n do
				local byte = buffer.readi8(stream, iterator)
				if endianness then
					val = val + byte * (2 ^ ((j - 1) * 8))
				else
					val = val + byte * (2 ^ ((n - j) * 8))
				end
				iterator = iterator + 1
			end

			if signed and val >= 2 ^ (n * 8 - 1) then
				val = val - 2 ^ (n * 8)
			end

			table.insert(vars, math.floor(val))
		elseif opt:find('[fd]') then
			local n = if (opt == 'd') then 8 else 4
			local x = --[[stream:sub(iterator, iterator + n - 1)]] buffer.readstring(stream, iterator, n)
			iterator = iterator + n

			if not endianness then
				x = string.reverse(x)
			end

			local sign = 1
			local mantissa = string.byte(x, (opt == 'd') and 7 or 3) % ((opt == 'd') and 16 or 128)
			for i = n - 2, 1, -1 do
				mantissa = mantissa * (2 ^ 8) + string.byte(x, i)
			end

			if string.byte(x, n) > 127 then
				sign = -1
			end

			local exponent = (string.byte(x, n) % 128) * ((opt == 'd') and 16 or 2) + math.floor(string.byte(x, n - 1) / ((opt == 'd') and 16 or 128))
			if exponent == 0 then
				table.insert(vars, 0.0)
			else
				mantissa = (math.ldexp(mantissa, (opt == 'd') and -52 or -23) + 1) * sign
				table.insert(vars, math.ldexp(mantissa, exponent - ((opt == 'd') and 1023 or 127)))
			end
		elseif opt == 's' then
			local bytes = {}
			for j = iterator, buffer.len(stream) do
				local val = buffer.readstring(stream, j, 1)
				if val == string.char(0) or val == '' then
					break
				end

				table.insert(bytes, val)
			end

			local str = table.concat(bytes)
			iterator = iterator + str:len() + 1
			table.insert(vars, str)
		elseif opt == 'c' then
			local val = buffer.readstring(stream, i + 1, 1)
			local n: string = (val:match('%d+') :: string)
			local len = (tonumber(n) :: number)
			if len <= 0 then
				len = (table.remove(vars) :: number)
			end

			val = buffer.readstring(stream, iterator, len)
			table.insert(vars, val)
			iterator = iterator + len
			i = i + n:len()
		end
	end

	return unpack(vars)
end
"""

JSON = """local json = {}
function json.loads(t)
    return game.HttpService:JSONEncode(t)
end
function json.dumps(t)
    return game.HttpService:JSONDecode(t)
end
function fault()
    error("[roblox-py] (json-lib) Outputting to files is not supported.")
end
json.load, json.dump = fault, fault"""

# libs = ["json"]

errs = [
    "ValueError",
    "TypeError",
    "AttributeError",
    "IndexError",
    "KeyError",
    "ZeroDivisionError",
    "AssertionError",
    "NotImplementedError",
    "RuntimeError",
    "NameError",
    "SyntaxError",
    "IndentationError",
    "TabError",
    "ImportError",
    "ModuleNotFoundError",
    "OSError",
    "FileNotFoundError",
    "PermissionError",
    "EOFError",
    "ConnectionError",
    "TimeoutError",
    "UnboundLocalError",
    "RecursionError",
    "MemoryError",
    "OverflowError",
    "FloatingPointError",
    "ArithmeticError",
    "ReferenceError",
    "SystemError",
    "SystemExit",
    "GeneratorExit",
    "KeyboardInterrupt",
    "StopIteration",
    "Exception",
    "BaseException",
    "Error",
]
libs = [
    "complex",
    "class",
    "dict",
    "__name__",
    "range",
    "len",
    "abs",
    "str",
    "int",
    "sum",
    "max",
    "min",
    "reversed",
    "split",
    "round",
    "all",
    "any",
    "ord",
    "chr",
    "callable",
    "float",
    "super",
    "format",
    "hex",
    "id",
    "map",
    "bool",
    "divmod",
    "slice",
    '__slicearr',
    "anext",
    "ascii",
    "dir",
    "getattr",
    "globals",
    "hasattr",
    "isinstance",
    "issubclass",
    "iter",
    "locals",
    "oct",
    "pow",
    "eval",
    "exec",
    "filter",
    "frozenset",
    "aiter",
    "bin",
    "deltaattr",
    "enumerate",
    "bytearray",
    "bytes",
    "compile",
    "help",
    "memoryview",
    "repr",
    "sorted",
    "vars",
]

DEPENDENCY = """\n\n--> imports
py = _G.rbxpy or require(game.ReplicatedStorage.Packages.pyruntime)
if game.ReplicatedStorage:FindFirstChild("Packages") and game.ReplicatedStorage.Packages:FindFirstChild("rcclib") then
    rcc = _G.rcc or require(game.ReplicatedStorage.Packages.rcclib)
else
    rcc = { }
    setmetatable(rcc, {__index = function(_, index) return function()end end})
end
"""

FN = """\n\nif game then
    __name__ = (if script:IsA("BaseScript") then "__main__" else script.Name)
    else
    __name__ = nil
    end
    range = function(s, e, f) -- range()
        local tb = {}
        local a = 0
        local b = 0
        local c = 0
        if not e then a=1 else a=s end
        if not e then b=s else b=e end
        if not f then c=1 else c=f end
        for i = a, b, c do
            tb[#tb+1] = i
        end
        return tb
    end
    len = function(x) return #x end -- len()
    abs = math.abs -- abs()
    str = tostring -- str()
    int = tonumber -- int()
    sum = function(tbl) --sum()
        local total = 0
        for _, v in ipairs(tbl) do
            total = total + v
        end
        return total
    end
    max = function(tbl) --max()
        local maxValue = -math.huge
        for _, v in ipairs(tbl) do
            if v > maxValue then
                maxValue = v
            end
        end
        return maxValue
    end
    min = function(tbl) --min()
        local minValue = math.huge
        for _, v in ipairs(tbl) do
            if v < minValue then
                minValue = v
            end
        end
        return minValue
    end
    reversed = function(xs, ...) -- reversed()
        local tmp = xs.copy()
        __call__(tmp.reverse, __kwargs__(), ...)

        return tmp
    end
    split = function(str, sep) -- split
        local substrings = {}
        local pattern = string.format("([^%s]+)",sep or "%s")
        for substring in string.gmatch(str, pattern) do
            table.insert(substrings, substring)
        end
        return substrings
    end
    round = math.round -- round()
    all = function (iter) -- all()
        for i, v in iter do if not v then return false end end

        return true
    end
    any = function (iter) -- any()
        for i, v in iter do
            if v then return true end
        end
        return false
    end
    ord = string.byte -- ord
    chr = string.char -- chr
    callable = function(fun) -- callable()
        if rawget(fun) ~= fun then warn("At the momement Roblox.py's function callable() does not fully support metatables.") end
        return typeof(rawget(fun))	== "function"
    end
    float = tonumber -- float()
    format = function(format, ...) -- format
        local args = {...}
        local num_args = select("#", ...)

        local formatted_string = string.gsub(format, "{(%d+)}", function(index)
            index = tonumber(index)
            if index >= 1 and index <= num_args then
                return tostring(args[index])
            else
                return "{" .. index .. "}"
            end
        end)

        return formatted_string
    end
    hex = function (value) -- hex
        return string.format("%x", value)
    end
    id = function (obj) -- id
        return print(tostring({obj}):gsub("table: ", ""):split(" ")[1])
    end
    map = function (func, ...) --map
        local args = {...}
        local result = {}
        local num_args = select("#", ...)

        local shortest_length = math.huge
        for i = 1, num_args do
            local arg = args[i]
            local arg_length = #arg
            if arg_length < shortest_length then
                shortest_length = arg_length
            end
        end

        for i = 1, shortest_length do
            local mapped_args = {}
            for j = 1, num_args do
                local arg = args[j]
                table.insert(mapped_args, arg[i])
            end
            table.insert(result, func(unpack(mapped_args)))
        end

        return result
    end
    bool = function(x) -- bool
        if x == false or x == nil or x == 0 then
            return false
        end
        
        if typeof(x) == "table" then
            if x._is_list or x._is_dict then
                return next(x._data) ~= nil
            end
        end

        return true
    end
    divmod = function(a, b) -- divmod
        local res = { math.floor(a / b), math.fmod(a, b) }
        return unpack(res)
    end
    slice = function (seq, start, stop, step)
        local sliced = {}
        local len = #seq
        start = start or 1
        stop = stop or len
        step = step or 1
        if start < 0 then
            start = len + start + 1
        end
        if stop < 0 then
            stop = len + stop + 1
        end
        for i = start, stop - 1, step do
            table.insert(sliced, seq[i])
        end
        return sliced
    end
    __slicearr = function (arr, start, stop, step)
        local arr_len = #arr

        if start < 0 then
            start += arr_len+1
        end

        if stop < 0 then
            stop += arr_len+1
        end

        local sliced
        if typeof(arr) == 'string' then
            sliced = ''
        else
            sliced = arr.copy()
            sliced.clear()
        end

        for i = start, stop-1, step do
            if typeof(arr) == 'string' then
                sliced ..= arr:sub(i+1, i+1)
                continue
            end

            sliced.append(arr[i])
        end

        return sliced
    end
    anext = function (iterator) -- anext
        local status, value = pcall(iterator)
        if status then
            return value
        end
    end
    ascii = function (obj) -- ascii
        return string.format("%q", tostring(obj))
    end
    dir = function (obj) -- dir
        local result = {}
        for key, _ in pairs(obj) do
            table.insert(result, key)
        end
        return result
    end
    getattr = function (obj, name, default) -- getattr
        local value = obj[name]
        if value == nil then
            return default
        end
        return value
    end
    globals = function () -- globals
        return _G
    end
    hasattr = function (obj, name) --hasattr
        return obj[name] ~= nil
    end
    isinstance = function (obj, class) -- isinstance
        if typeof(obj) ~= 'table' then
            return false
        end

        local mt = getmetatable(obj)
        if class and typeof(class) == 'table' then
            if class._is_list_class then
                return obj._is_list == true
            elseif class._is_dict_class then
                return obj._is_dict == true
            end
        end

        if typeof(obj) == "table" and mt and mt._class then
            if mt._class == class then
                return true
            end

            return issubclass(mt._class, class)
        end 

        return type(obj) == class
    end
    issubclass = function (cls, classinfo) -- issubclass
        if (typeof(cls) ~= "table") or (not getmetatable(cls)) or (not cls._bases) then
            return false
        end

        for _, b in cls._bases do
            if b == classinfo then
                return true
            end
        end

        return false
    end
    iter = function (obj) -- iter
        if type(obj) == "table" and obj.__iter__ ~= nil then
            return obj.__iter__
        end
        return nil
    end
    locals = function () -- locals
        return _G
    end
    oct = function (num) --oct
        return string.format("%o", num)
    end
    pow = function (base, exponent, modulo) --pow
        if modulo ~= nil then
            return math.pow(base, exponent) % modulo
        else
            return base ^ exponent
        end
    end
    eval = function (expr, env)
        return loadstring(expr)()
    end
    exec = loadstring
    filter = function (predicate, iterable)
        local result = {}
        for _, value in ipairs(iterable) do
            if predicate(value) then
                table.insert(result, value)
            end
        end
        return result
    end
    frozenset = function (...)
        local elements = {...}
        local frozenSet = {}
        for _, element in ipairs(elements) do
            frozenSet[element] = true
        end
        return frozenSet
    end
    aiter = function (iterable) -- aiter
        return pairs(iterable)
    end
    bin = function(num: number)
        local bits = {}
        repeat
            table.insert(bits, 1, num % 2)
            num = math.floor(num / 2)
        until num == 0
        return "0b" .. table.concat(bits)
    end

    deltaattr = function (object, attribute) -- delattr
        object[attribute] = nil
    end

    enumerate = function (t)
        local i = 0
        return function()
            i += 1

            local value = t(nil, i)
            if value ~= nil then
                return i-1, value
            end
        end
    end

    bytearray = function (arg) -- bytearray
        if type(arg) == "string" then
            local bytes = {}
            for i = 1, #arg do
                table.insert(bytes, string.byte(arg, i))
            end
            return bytes
        elseif type(arg) == "number" then
            local bytes = {}
            while arg > 0 do
                table.insert(bytes, 1, arg % 256)
                arg = math.floor(arg / 256)
            end
            return bytes
        elseif type(arg) == "table" then
            return arg -- Assuming it's already a bytearray table
        else
            error("Invalid argument type for bytearray()")
        end
    end
    bytes = function (arg) -- bytes
        if type(arg) == "string" then
            local bytes = {}
            for i = 1, #arg do
                table.insert(bytes, string.byte(arg, i))
            end
            return bytes
        elseif type(arg) == "table" then
            return arg -- Assuming it's already a bytes table
        else
            error("Invalid argument type for bytes()")
        end
    end
    compile = loadstring
    help = function (object) -- help
        print("Help for object:", object)
        print("Type:", type(object))
        print("Learn more in the official roblox documentation!")
    end
    memoryview = function (object) -- memoryview
        if type(object) == "table" then
            local buffer = table.concat(object)
            return { buffer = buffer, itemsize = 1 }
        else
            error("Invalid argument type for memoryview()")
        end
    end
    repr = function (object) -- repr
        return tostring(object)
    end
    sorted = function (xs, ...) -- sorted
        local tmp = xs.copy()
        __call__(tmp.sort, __kwargs__(), ...)

        return tmp
    end
    vars = function (object) -- vars
        local attributes = {}
        for key, value in pairs(object) do
            attributes[key] = value
        end
        return attributes
    end"""

CLASS = """\n\n
_G.__super_stack = _G.__super_stack or {}

function class(class_init, bases)
        bases = bases or {}

        local c = {}
        local staticMethods = {}

        c._bases = bases
        c = class_init(c, staticMethods)

        -- this is to allow the below edge case:
        -- class Base():
        --     name = "Base"
        -- class Foo(Base):
        --     pass
        -- print(Foo.name)
        -- so that it prints "Base"
        for _, b in ipairs(bases) do
            for k, v in pairs(b.__static) do
                if not staticMethods[k] then
                    staticMethods[k] = v
                end
            end
        end

        local mt = getmetatable(c) or {}
        mt.__index = function(_, k)
            if k == '__static' then
                return staticMethods
            end

            local method = staticMethods[k];
            if method then
                return method;
            end

            return rawget(c, k);
        end

        mt.__call = function(_, ...)
            local object = {}

     	    local meta = {
                _class = c,
                _bases = bases,
                __add = c.__add__,
                    __sub = c.__sub__,
                    __mul = c.__mul__,
                    __div = c.__div__,
                    __pow = c.__pow__,
                __unm = c.__unm,
                __tostring = c.__str__,
                __index = function(tbl, idx)
                    local method = c[idx]
                    if typeof(method) == "function" then
                        return function(...)
                            table.insert(_G.__super_stack, object)
                            local res = c[idx](object, ...) 
                            table.remove(_G.__super_stack)

                            return res
                        end
                    end

                    for _, base in ipairs(bases) do
                        local base_method = base[idx]
                        if typeof(base_method) == "function" then
                            return function(...)
                                table.insert(_G.__super_stack, object)
                                local res = base_method(object, ...)
                                table.remove(_G.__super_stack)
                                return res
                            end
                        elseif base_method ~= nil then
                            return base_method
                        end
                    end

                    return method
                end,
	        }

            for k, v in pairs(c) do
                if #k > 3 and k:sub(1, 2) == "__" and not meta[k] then
                    -- to support things like __eq__
                    meta[k] = v
                end
            end

            local lu = {
                __add__ = "__add",
                __sub__ = "__sub",
                __mul__ = "__mul",
                __div__ = "__div",
                __pow__ = "__pow",
                __unm__ = "__unm",
                __str__ = "__tostring"
            }
            for _, b in ipairs(bases) do
                for k, v in pairs(lu) do
                    local f = b[k]
                    if (not f) or meta[v] then
                        continue
                    end

                    meta[v] = f
                end
            end

            setmetatable(object, meta)
            if object.__init__ then
                local override = object.__init__(...)
                if override ~= nil then
                    return override
                end
            end
            return object
        end

        setmetatable(c, mt)

        return c
    end
function super()
    local self = _G.__super_stack[#_G.__super_stack]
    local mt = getmetatable(self)
    assert(typeof(mt) == "table" and mt._bases, "super() called outside of class instance")

    local bases = mt._class and mt._class._bases or {}
    
    local proxy = {}
    setmetatable(proxy, {
        __index = function(_, key)
            for _, base in ipairs(bases) do
                local method = base[key]
                if typeof(method) == "function" then
                    return function(...)
                        return method(self, ...)
                    end
                elseif method ~= nil then
                    return method
                end
            end
            return nil
        end
    })
    return proxy
end"""
DICT = """\n\n
dict = {}

function dict_impl(t)
        local result = {}

        result._is_dict = true

        result._data = {}
        for k, v in pairs(t) do
            result._data[k] = v
        end

        local methods = {}

        local key_index = nil

        methods.reverse = function()
            local rev = {}
            for k, v in result._data do
                rev[v] = k
            end

            return dict(rev)
        end

        methods.clear = function()
            result._data = {}
        end

        methods.copy = function()
            return dict(result._data)
        end

        methods.get = function(key, default)
            default = default or nil
            if result._data[key] == nil then
                return default
            end

            return result._data[key]
        end

        methods.items = function()
            return pairs(result._data)
        end

        methods.keys = function()
            local keys = list({})
            for k, v in result._data do
                keys.append(k)
            end

            return keys
        end

        methods.values = function()
            local values = list({})
            for k, v in result._data do
                values.append(v)
            end

            return values
        end

        methods.pop = function(key, default)
            default = default or nil
            if result._data[key] ~= nil then
                local value = result._data[key]
                result._data[key] = nil 
                return key, value
            end

            return key, default
        end

        methods.popitem = function()
            local key, value = next(result._data)
            if key ~= nil then
                result._data[key] = nil
            end

            return key, value
        end

        methods.setdefault = function(key, default)
            if result._data[key] == nil then
                result._data[key] = default
            end

            return result._data[key]
        end

        methods.update = function(t)
            assert(t._is_dict)

            for k, v in t.items() do
                result._data[k] = v
            end
        end

        setmetatable(result, {
            __index = function(self, index)
                if result._data[index] ~= nil then
                    return result._data[index]
                end
                return methods[index]
            end,
            __newindex = function(self, index, value)
                result._data[index] = value
            end,
            __call = function(self, _, idx)
                if idx == nil and key_index ~= nil then
                    key_index = nil
                end

                key_index, v = next(result._data, key_index)

                return key_index, v
            end,
        })

        return result
end

dict = setmetatable({_is_dict_class=true}, {
    __call = function(self, ...)
        return dict_impl(...)
    end,  
})

if not _G._list_mt then
    _G._list_mt = {}
end

list = {}

function list_impl(raw)
    raw = raw or {}

    local methods = {}
    local mt = getmetatable(raw) or {}

    function methods.copy()
        return list(table.clone(raw))
    end

    function methods.append(x)
        table.insert(raw, x)
    end

    function methods.extend(xs)
        for _, x in xs do
            table.insert(raw, x)
        end
    end

    function methods.pop(i)
        if i ~= nil then
            return table.remove(raw, i+1)
        end

        return table.remove(raw)
    end

    function methods.clear()
        table.clear(raw)
    end

    function methods.insert(y, z)
        table.insert(raw, y+1, z)
    end

    function methods.remove(el)
        table.remove(raw, table.find(raw, el))
    end

    function methods.sort(key, reverse)
        local kwargs = __kwargs__()
        key = kwargs.get('key') or key
        reverse = kwargs.get('reverse') or reverse

        if key == nil then
            key = function(x)
                return x
            end
        end

        local function ascending(a, b)
            return key(a) > key(b)
        end

        local function descending(a, b)
            return key(a) < key(b)
        end

        local f = ascending
        if reverse then
            f = descending
        end

        table.sort(raw, f)
    end

    function methods.find(x, y)
        if y ~= nil then
            return table.find(raw, x, y)
        end

        return table.find(raw, x)
    end

    function methods.index(el)
        local a = table.find(raw, el)
        if typeof(a) ~= 'number' then
            return nil
        end

        return a-1
    end

    function methods.reverse()
        for i = 1, math.floor(#raw / 2) do
            raw[i], raw[#raw-i + 1] = raw[#raw-i + 1], raw[i]
        end
    end

    function methods.extend(xs)
        for _, x in xs do
            table.insert(raw, x)
        end
    end

    function methods.raw()
        return raw
    end

    mt._is_list = true
    mt._data = raw

    function mt:__len()
        return #raw
    end

    function mt:__tostring()
        local str = '['

        for i, v in ipairs(raw) do
            if typeof(v) == 'string' then
                v = `'{v}'`
            end

            str ..= tostring(v)

            if i < #raw then
                str ..= ', '
            end
        end

        return str..']'
    end

    function mt:__index(i)
        if i == '_is_list' then
            return true
        end

        if methods[i] ~= nil then
            return methods[i]
        end

        if typeof(i) ~= 'number' then
            return nil
        end

        if i < 0 then
            i = #raw + i
        end

        return raw[i+1]
    end

    function mt:__eq__(x)
        assert(typeof(x) == "table" and x._is_list)

        if #raw ~= #x then
            return false
        end

        for i = 0, #raw-1 do
            if raw[i+1] ~= x[i] then
                return false
            end
        end

        return true
    end

    function mt:__add(b)
        local cpy = methods.copy()
        cpy.extend(b)

        return cpy
    end

    function mt:__newindex(i, v)
        raw[i+1] = v
    end

    function mt:__iter()
        local function iter(state, i)
            i += 1
            local v = state[i + 1]
            if v ~= nil then
                return i, v
            end
        end

        return iter, raw, -1
    end

    local k, v = nil, nil
    function mt:__call(_, i)
        if i == nil and k ~= nil then
            k = nil
        end

        k, v = next(raw, k)
        return v
    end

    return setmetatable({}, mt)
end

list = setmetatable({_is_list_class=true}, {
    __call = function(self, ...)
        return list_impl(...)
    end,
})

function __unpack__(exp, ...)
    local args = {...}

    if (#args == 1) and (typeof(args[1]) == 'table') and (args[1]._is_list == true) then
        if exp > 0 then
            assert(#args[1] == exp, `expected {exp} values to unpack, got {#args[1]}`)
        end

        return unpack(args[1].raw())
    end

    if exp > 0 then
        assert(#args == exp, `expected {exp} values to unpack, got {#args}`)
    end
    
    return ...
end
"""

GENERATOR = """\n\nlocal __PY_GENERATORS = {}
function yieldGenerator(name, value)
    if not __PY_GENERATORS[name] then
        error("[roblox-py]: Attempt to yield a generator that is not being iterated over.")
    end
    table.insert(__PY_GENERATORS[name], value)
end
function generatorLoop(name, func)
    if not __PY_GENERATORS[name] then
        __PY_GENERATORS[name] = {}
    end
    return function(loopFunc)
        local DONE = false
		local currentSize = 0
		task.spawn(function()
			func()
            table.insert(__PY_GENERATORS[name], "__END")
		end)
		while (not DONE) and task.wait() do
			if #__PY_GENERATORS[name] > currentSize then
				for i = currentSize + 1, #__PY_GENERATORS[name] do
					if __PY_GENERATORS[name][i] == "__END" then
                        DONE = true
                        break
                    end
					
					local v = __PY_GENERATORS[name][i]
					loopFunc(i-1, v)
				end
				currentSize = #__PY_GENERATORS[name]
			end
		end
    end
end
"""

OVERLOADS = """\n\n

function __eq__(x, y)
    if typeof(x) == "table" and typeof(y) == "table" and getmetatable(x)
        and getmetatable(x).__eq__ ~= nil
    then
        return getmetatable(x).__eq__(x, y)
    end

    return x == y
end

function __add__(a, b)
    at = typeof(a)
    bt = typeof(b)

    if at == 'string' and bt == 'string' then
        return a .. b
    end

    if (at == 'table') and (getmetatable(a)) and (getmetatable(a).__add) then
        return getmetatable(a).__add(a, b)
    end

    return a+b
end

function __in__(xs, x)
    if typeof(xs) == 'string' then
        return string.find(xs, x, 1, true) ~= nil
    end

    if xs._is_list then
        return xs.find(x) ~= nil
    end

    return xs[x] ~= nil
end

"""

KWARGS = """\n\n
_G.__kwargs_stack = _G.__kwargs_stack or {}

function __call__(f, kwargs, ...)
    table.insert(_G.__kwargs_stack, kwargs or {})
    local res = table.pack(f(...))
    table.remove(_G.__kwargs_stack)

    return unpack(res)
end

function __kwargs_raw__()
    return _G.__kwargs_stack[#_G.__kwargs_stack]
end

function __kwargs__()
    return dict(__kwargs_raw__())
end

-- for ** in kwarg functions (i.e. foo(bar='baz', **{'hi': 'ho'}) = {bar='baz', hi='ho'}) with multiple kwargs
function __merge__(a, b)
    local c = {}

    for k, v in a do
        c[k] = v
    end
 
    for k, v in b do
        c[k] = v
    end

    return c
end
"""