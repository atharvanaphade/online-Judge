#include <bits/stdc++.h>
#define ll long long
#define test unsigned int t;t = 1;while(t--)
#define fr(n) for(i = 0 ; i < n ; i++)
#define fre(n) for(i = 1 ; i <= n ; i++)
#define pn(x) cout << x <<"\n";
#define ln cout << "\n";
#define ps(x) cout << x <<" ";
#define pb push_back
#define fastio ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0);
using namespace std;

int main()
{
    fastio

    ll n, i;

    test
    {
        ll ans=0;
        cin >> n;
        if(n < 0)
        {
            pn("Invalid Input")
            return 0;
        }
        if(n&1)
        {
            while(n != 0)
            {
                ll r = n%10;
                ans+=r;
                n/=10;
            }
        }
        else
        {
            ans= 1;
            while(n != 0)
            {
                ll r = n%10;
                ans*=r;
                n/=10;
            }
        }
        pn(ans)
    }


    return 0;
}
