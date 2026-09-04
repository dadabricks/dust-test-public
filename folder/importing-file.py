from libraries.gen_hello import gen_hello

# 'libraries' lives at the Git folder root, not next to this file, so this import only
# resolves when the repo root is on sys.path (PROD-53738). Plain .py files -- unlike this
# file's sibling notebook -- did not get that behavior before the fix.
res = gen_hello("Ala")
print(res)
assert res == "Hello Ala", f"unexpected result from gen_hello: {res}"
