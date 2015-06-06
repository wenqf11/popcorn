package cn.edu.tsinghua.thss.popcorn;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.ListView;
import android.widget.SearchView;
import android.widget.TextView;

import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.view.annotation.ViewInject;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class DeviceInfoSearchActivity extends Activity implements
        SearchView.OnQueryTextListener{

    private List<Map<String, Object>> mData = null;
    private SearchListAdapter searchAdapter;
    private SearchView searchView;
    private ArrayList<String> names;
    private HintAdapter adapter;
    private ArrayList<String> mAllList = new ArrayList<String>();

    @ViewInject(R.id.device_info_listview)
    private ListView resultListView ;

    @ViewInject(R.id.device_info_hint_listview)
    private ListView hintListView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_info_search);

        ViewUtils.inject(this);

        initActionbar();
        initListViewandAapter();
    }

    private void initListViewandAapter(){
        names = loadData();

        adapter = new HintAdapter(this, names);
        hintListView.setAdapter(adapter);
        hintListView.setTextFilterEnabled(true);
        searchView.setOnQueryTextListener(this);

        searchAdapter = new SearchListAdapter (this);
        resultListView.setAdapter(searchAdapter);

        hintListView.setOnItemClickListener(new AdapterView.OnItemClickListener(){

            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id)
            {
                searchView.setQuery(adapter.getItem(position).toString(), true);
            }
        });

        resultListView.setOnItemClickListener(new AdapterView.OnItemClickListener(){

            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id)
            {
                Intent intent = new Intent(getApplicationContext(), DeviceInfoDetailActivity.class);
                Bundle bundle = new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
            }
        });
    }

    private void initActionbar() {
        // 自定义标题栏
        getActionBar().setDisplayShowHomeEnabled(false);
        getActionBar().setDisplayShowTitleEnabled(false);
        getActionBar().setDisplayShowCustomEnabled(true);
        Drawable draw=this.getResources().getDrawable(R.drawable.actionbar_bg);
        getActionBar().setBackgroundDrawable(draw);

        LayoutInflater mInflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View mTitleView = mInflater.inflate(R.layout.custom_action_bar_layout, null);
        getActionBar().setCustomView(
                mTitleView,
                new ActionBar.LayoutParams(ActionBar.LayoutParams.MATCH_PARENT,
                        ActionBar.LayoutParams.WRAP_CONTENT));
        searchView = (SearchView) mTitleView.findViewById(R.id.search_view);
    }

    public ArrayList<String> loadData() {
        mAllList.add("aa");
        mAllList.add("ddfa");
        mAllList.add("qw");
        mAllList.add("sd");
        mAllList.add("CD");
        mAllList.add("cf");
        mAllList.add("开始");
        return mAllList;
    }

    public class HintAdapter extends BaseAdapter implements Filterable{

        private LayoutInflater mInflater = null;
        private HintHolder holder = null;
        public ArrayList<String> nameList = null;
        public ArrayList<String> originNameList = null;

        public HintAdapter(Context context, ArrayList<String> data) {
            super();
            this.nameList = data;
            this.originNameList = data;
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        public class HintHolder
        {
            TextView name;
        }

        @Override
        public int getCount() {
            // TODO Auto-generated method stub
            //return emp_list.size();
            if(nameList == null){
                return 0;
            }else{
                return nameList.size();
            }
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return nameList.get(position);
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public Filter getFilter() {
            return new Filter() {

                @Override
                protected FilterResults performFiltering(CharSequence constraint) {
                    final FilterResults oReturn = new FilterResults();
                    final ArrayList<String> results = new ArrayList<String>();

                    if (constraint != null) {
                        if (originNameList != null && originNameList.size() > 0) {
                            for (final String st : originNameList) {
                                if (st.toLowerCase()
                                        .contains(constraint.toString().toLowerCase()))
                                    results.add(st);
                            }
                        }
                        oReturn.values = results;
                    }
                    return oReturn;
                }

                @SuppressWarnings("unchecked")
                @Override
                protected void publishResults(CharSequence constraint,
                                              FilterResults results) {
                    nameList = (ArrayList<String>) results.values;
                    notifyDataSetChanged();
                }
            };
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            // TODO Auto-generated method stub

            if(convertView==null)
            {
                convertView=mInflater.inflate(R.layout.listview_search_hint, parent, false);
                holder = new HintHolder();
                holder.name=(TextView) convertView.findViewById(R.id.listview_search_hint_name);
                convertView.setTag(holder);
            }
            else
            {
                holder = (HintHolder) convertView.getTag();
            }

            holder.name.setText(nameList.get(position));

            return convertView;

        }

    }



    private List<Map<String, Object>> getData(String[] str_name, String[] str_dept, String[] str_credit) {
        List<Map<String ,Object>> list = new ArrayList<Map<String,Object>>();

        for (int i = 0; i < str_dept.length; i++) {
            Map<String, Object> map = new HashMap<String, Object>();
            map.put("name", str_name[i]);
            map.put("dept", str_dept[i]);
            map.put("credit", str_credit[i]);
            list.add(map);
        }

        return list;
    }


    public class SearchListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;
        private ViewHolder holder = null;

        private class ViewHolder {
            public TextView name;
            public TextView dept;
            public TextView credit;
        }
        public SearchListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            if (mData == null){
                return 0;
            }else{
                return mData.size();
            }
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            if (convertView == null) {
                holder = new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_rank, null);

                holder.name = (TextView) convertView.findViewById(R.id.listview_rank_name);
                holder.dept = (TextView) convertView.findViewById(R.id.listview_rank_dept);
                holder.credit = (TextView) convertView.findViewById(R.id.listview_rank_credit);
                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.name.setText((String)mData.get(position).get("name"));
            holder.dept.setText((String)mData.get(position).get("dept"));
            holder.credit.setText((String)mData.get(position).get("credit"));

            return convertView;
        }
    }


    //用户输入字符时激发该方法
    @Override
    public boolean onQueryTextChange(String newText) {
        resultListView.setVisibility(View.GONE);
        hintListView.setVisibility(View.VISIBLE);
        if (TextUtils.isEmpty(newText)) {
            HintAdapter ca = (HintAdapter)hintListView.getAdapter();
            ca.getFilter().filter("");
        } else {
            HintAdapter ca = (HintAdapter)hintListView.getAdapter();
            ca.getFilter().filter(newText);
        }
        return false;
    }
    //单击搜索按钮时激发该方法
    @Override
    public boolean onQueryTextSubmit(String query) {
        hintListView.setVisibility(View.GONE);
        resultListView.setVisibility(View.VISIBLE);
        String[] str_name = {"黄小明","王小明","小明","赵小明","孙小明","钱小明","李小明","李小明","李小明"};
        String[] str_dept = {"微谷项目部","天坛项目部","天坛项目部","微谷项目部","微谷项目部","微谷项目部","微谷项目部","天坛项目部","天坛项目部"};
        String[] str_credit = {"140","120","110","90","80","60","50","50","50"};
        mData = getData(str_name, str_dept, str_credit);
        searchAdapter.notifyDataSetChanged();
        return false;
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.device_info_search, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.search_btn) {
            searchView.setQuery(searchView.getQuery(), true);
        }
        return super.onOptionsItemSelected(item);
    }
}
